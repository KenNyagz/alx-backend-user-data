#!/usr/bin/env python3
'''

'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''takes in a password string arguments and returns bytes'''
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
