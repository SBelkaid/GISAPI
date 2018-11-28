from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Enum
from passlib.hash import sha256_crypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from collections import OrderedDict
import decimal
import datetime


Base = declarative_base()
DATABASE_URI = 'sqlite.db'
engine = create_engine('sqlite:///' + DATABASE_URI)
Session = sessionmaker(bind=engine)


class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class User(Base, UserMixin, DictSerializable):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(128))
    role = Column(Enum('moderator', 'surveyor', 'client'))

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        # password is hashed when set by __init__, afterwards not readable.

    @password.setter
    def password(self, password):
        # self.password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        self.password_hash = sha256_crypt.hash(password)

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def __repr__(self):
        return "<User(id=%s, name='%s', lastname='%s', role='%s')>" % (
            self.id, self.first_name, self.last_name, self.role)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        #used to be return self.login
        return self.login




