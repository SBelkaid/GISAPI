from datetime import datetime
import sqlite3 as sq
from sqlalchemy import create_engine
from models import User, Base
from sqlalchemy.orm import sessionmaker


DATABASE_URI = 'sqlite.db'

engine = create_engine('sqlite:///'+DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    # Create the list of people from our data
    set_up_db()
    print session.query(User, User.first_name).all()
    return 200


def set_up_db():
    if not engine.dialect.has_table(engine, 'users'):
        Base.metadata.create_all(engine)


def add_user(firstname, lastname, email, password):
    """
    This function should make it possible to add a user to the database
    :return: None
    """
    set_up_db() #just to make sure the table exists
    session = Session()
    try:
        u = User(first_name=firstname, last_name=lastname, email=email, password=password)
        session.add(u)
        session.commit()
        session.close()
    except sq.IntegrityError, e:
        print("IntegrityError, {}".format(e))