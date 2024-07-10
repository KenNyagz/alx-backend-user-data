#!/usr/bin/env python3
'''
basic authentication
'''
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
