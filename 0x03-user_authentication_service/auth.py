#!/usr/bin/env python3
'''
Authentication handling
'''
import uuid
import bcrypt
# from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import NoResultFound
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
                                       user.hashed_password.encode('utf-8')):
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception:
            return False
