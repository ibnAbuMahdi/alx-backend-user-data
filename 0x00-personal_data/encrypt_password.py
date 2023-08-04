#!/usr/bin/env python3
""" encrypt password module a b c d ef g """
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns salted, hashed password as byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check whether hashed_password matches password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
