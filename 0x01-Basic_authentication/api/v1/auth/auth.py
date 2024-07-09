#!/usr/bin/env python3
'''
managing authentications
'''
from flask import request
from typing import List

class Auth:
    '''Class to manage API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Prompts the client authentication '''
        return False

    def authorization_header(self, request=None) -> str:
        '''Sets authorizations headers '''
        return None

    def current_user(self, request=None) -> TypeVar:
        '''gets current user information '''
        return None
