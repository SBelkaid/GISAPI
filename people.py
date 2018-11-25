from datetime import datetime
import sqlite3 as sq
from passlib.hash import sha256_crypt

DATABASE_URI = '/tmp/sqlite.db'
conn = sq.connect(DATABASE_URI)
c = conn.cursor()


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "email": "amaial@mail.nl",
        "lname": "Farrell",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "email": "amaisl@mail.nl",
        "lname": "Brockman",
        "timestamp": get_timestamp()
    },
    "Easter": {
        "fname": "Bunny",
        "email": "amaidl@mail.nl",
        "lname": "Easter",
        "timestamp": get_timestamp()
    }
}


# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    # Create the list of people from our data
    set_up_db()
    with sq.connect(DATABASE_URI) as conn:
        c = conn.cursor()
        return c.execute("select * from user").fetchall()



def set_up_db():
    with sq.connect(DATABASE_URI) as conn:
        c = conn.cursor()
        user_table = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';").fetchall()
        print user_table
        if not user_table:
            create_statement = """create table user (
              id integer primary key autoincrement,
              firstname text not null,
              lastname text not null,
              email text not null,
              password_hash text not null,
              unique (email)
            );"""
            c.execute(create_statement)
        conn.commit()


def add_user(firstname, lastname, email, password):
    """
    This function should make it possible to add a user to the database
    :return: None
    """
    set_up_db() #just to make sure the table exists
    with sq.connect(DATABASE_URI) as conn:
        c = conn.cursor()
        hashed_pw = sha256_crypt.hash(password)
        try:
            c.execute("INSERT INTO user (firstname, lastname, email, password_hash) VALUES (?,?,?,?)",\
                      (firstname, lastname, email, hashed_pw))
            conn.commit()
        except sq.IntegrityError, e:
            print("IntegrityError, {}".format(e))



