#!/usr/bin/env python3
'''
hasing passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''password hashing func'''
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    return hashed_pw
