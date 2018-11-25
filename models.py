from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from passlib.hash import sha256_crypt
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(128))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.first_name

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
