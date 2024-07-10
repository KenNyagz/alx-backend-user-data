#!/usr/bin/env python3
'''
managing authentications
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''Class to manage API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Prompts the client authentication '''
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        excluded_paths = [exl_pth if exl_pth.endswith('/') else exl_pth + '/'
                          for exl_pth in excluded_paths]

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''Sets authorizations headers '''
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar:
        '''gets current user information '''
        return None
