#!/usr/bin/env python3
'''
hasing passwords'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''password hashing func'''
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    return hashed_pw

def is_valid(encrpd_pw: bytes, password: str) -> bool:
    '''checks if the password entered is correct'''
    if bcrypt.checkpw(password.encode(), encrpd_pw):
        return True
    else:
        return False
