#!/usr/bin/env python3
""" The authentication module """
import bcrypt
import uuid
from db import DB
from typing import (TypeVar)
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a new user and return the user instance """
        try:
            found = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound as e:
            h_pwd = _hash_password(password)
            return self._db.add_user(email, h_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ determines the validity of @pwd """
        try:
            found = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  found.hashed_password)
        except NoResultFound as e:
            return False
        return False

    def create_session(self, email: str) -> str:
        """ creates and return a session id for user with @email """
        try:
            found = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            self._db.update_user(found.id, session_id=s_id)
            return s_id
        except NoResultFound as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """ returns a User that corresponds to @session_id """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroys a user session with id @user_id """
        if user_id is None:
            return None
        try:
            found = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ sets and return a password return token of a user """
        try:
            found = self._db.find_user_by(email=email)
            r_tkn = _generate_uuid()
            self._db.update_user(found.id, reset_token=r_tkn)
            return r_tkn
        except NoResultFound as e:
            raise ValueError

    def update_password(self, r_tkn: str, pwd: str) -> None:
        """ updates a user password """
        try:
            found = self._db.find_user_by(reset_token=r_tkn)
            h_pwd = _hash_password(pwd)
            self._db.update_user(found.id, hashed_password=h_pwd,
                                 reset_token=None)
        except NoResultFound as e:
            raise ValueError


def _generate_uuid() -> str:
    """ generates a new uuid """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """ returns a salted hash of the @pwd """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
