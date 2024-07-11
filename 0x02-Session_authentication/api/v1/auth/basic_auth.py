#!/usr/bin/env python3
'''
basic authentication
'''
import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''Basic authentiction management class'''
    def extract_base64_authorization_header(self, authrztn_header: str) -> str:
        '''returns the Base64 part of Authorization header for Basic Auth'''
        if not authrztn_header:
            return None
        if type(authrztn_header) is not str:
            return None
        if not authrztn_header.startswith('Basic '):
            return None
        return authrztn_header[len('Basic '):]

    def decode_base64_authorization_header(self,
                                           base64_authrztn_header: str) -> str:
        ''' returns the decoded value of a Base64 string'''
        if not base64_authrztn_header:
            return None
        if not isinstance(base64_authrztn_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authrztn_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        '''returns the user email and password from the Base64 decoded val'''
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves the User instance for a request:'''
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        decode_auth = self.decode_base64_authorization_header(base64_auth)
        user_email, user_pwd = self.extract_user_credentials(decode_auth)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
