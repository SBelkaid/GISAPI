from datetime import datetime
import sqlite3 as sq
from models import User, Base
from models import engine, Session
from flask_jwt import JWT, jwt_required, current_identity
from flask import g, abort
import functools
import json


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def is_moderator(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        # print current_identity
        if current_identity[0].role != 'moderator':
            abort(403)
        # invoke the wrapped function
        return f(*args, **kwargs)
    return wrap


# Create a handler for our read (GET) people
@jwt_required()
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    request_identity = current_identity[0]
    print 'Hello {}, email: {} role: {}'.format(request_identity.first_name,\
                                                request_identity.email, request_identity.role)
    session = Session()
    res = session.query(User.email).all()
    session.close()
    return json.dumps([dict(r._asdict()) for r in res])


def set_up_db():
    if not engine.dialect.has_table(engine, 'users'):
        Base.metadata.create_all(engine)
        print "Database created"
    print "Database already exists"


@jwt_required()
@is_moderator
def add_user(firstname, lastname, email, password, role):
    """
    This function should make it possible to add a user to the database
    :return: None
    """
    # set_up_db()  # just to make sure the table exists
    session = Session()
    try:
        u = User(first_name=firstname, last_name=lastname, email=email, password=password, role=role)
        session.add(u)
        session.commit()
        session.close()
    except sq.IntegrityError, e:
        print("IntegrityError, {}".format(e))
        return 404


# @jwt_required()
# @is_moderator
# def change_user_role(email, new_role):
#     """
#     This function should make it possible to change a user's role
#     :return: None
#     """
#     # set_up_db()  # just to make sure the table exists
#     session = Session()
#     try:
#         session.query(User).filter(User.email == email).\
#             update({"role": (User.role == new_role)})
#         session.commit()
#     except sq.IntegrityError, e:
#         print("IntegrityError, {}".format(e))
#         return 404


def verify_password(username, password):
    session = Session()
    search_result = session.query(User).filter(User.email == username).all()
    if not search_result or not search_result[0].verify_password(password):
        return False
    g.user = search_result[0]
    session.close()
    return g.user


def identity(payload):
    session = Session()
    user_id = payload['identity']
    user = session.query(User).filter(User.id == user_id)
    session.close()
    return user
