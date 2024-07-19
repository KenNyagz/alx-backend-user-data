#!/usr/bin/env python3
'''
Authentication handling
'''
import uuid
import bcrypt
from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _generate_uuid() -> str:
    '''generates uuid'''
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    '''takes in a password string arguments and returns bytes'''
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Registers a new user and return the created user '''
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''validates user by password if exists'''
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception:
            return False

    def create_session(self, email):
        '''creates session, returns stringified session_id'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return str(session_id)
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        '''return user based on on corresponding session_id'''
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        '''destroys a user session'''
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email):
        '''sets reset token attribute for user with corresponding email'''
        try:
            user = self._db.find_user_by(email=email)
            new_sessionID = _generate_uuid()
            self._db.update_user(user.id, reset_token=new_sessionID)
        except NoResultFound:
            raise ValueError('No user with email {email}')
        return new_sessionID

    def update_password(self, reset_token, password):
        '''gets user with correspoding reset_token uuid, updates password'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            salt = bcrypt.gensalt()
            hashed_p = bcrypt.hashpw(password.encode('utf-8'), salt)
            self._db.update_user(user.id, hashed_password=hashed_p,
                                 reset_token=None)
            return
        except NoResultFound:
            raise ValueError
