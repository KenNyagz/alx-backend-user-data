#!/usr/bin/env python3
'''
Session authentication
'''
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''Session authentication management class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' returns a User ID based on a Session ID'''
        if session_id is None or not isinstance(session_id, str):
            return None
        userID = self.user_id_by_session_id.get(session_id)
        return userID

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value: -oveload'''
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        '''deletes user session- logout'''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
