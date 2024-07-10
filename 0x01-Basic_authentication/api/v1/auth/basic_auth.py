#!/usr/bin/env python3
'''
basic authentication
'''
import base64
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
