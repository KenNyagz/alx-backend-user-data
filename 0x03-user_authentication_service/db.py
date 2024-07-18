#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''saves user to db and returns the user'''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''returns first row found in users table as filtered by input args'''
        if not kwargs:
            raise NoResultFound

        valid_keys = ['email', 'id', 'hashed_password', 'session_id',
                      'reset_token']
        for key in kwargs:
            if key not in valid_keys:
                raise InvalidRequestError

        search = self._session.query(User)
        for key in kwargs:
            if key == 'email':
                result = search.filter(User.email == kwargs[key])
            elif key == 'id':
                result = search.filter(User.id == kwargs[key])
            elif key == 'hashed_password':
                result = search.filter(User.hashed_password == kwargs[key])
            elif key == 'session_id':
                result = search.filter(User.session_id == kwargs[key])
            elif key == 'reset_token':
                result = search.filter(User.reset_token == kwargs[key])

        all_users =  result.all()
        if not all_users:
            raise NoResultFound
        return all_users[0]
          
