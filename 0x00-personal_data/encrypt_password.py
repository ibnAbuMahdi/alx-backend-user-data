#!/usr/bin/env python3
""" encrypt password """
import bcrypt


def hash_password(password: str) -> str:
    """ returns salted, hashed password as byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check whether hashed_password matches password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
