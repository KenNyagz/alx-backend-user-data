#!/usr/bin/env python3
'''
basic authentication
'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''Basic authentiction management class'''
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        '''returns the Base64 part of Authorization header for Basic Auth'''
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
