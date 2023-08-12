#!/usr/bin/env python3
""" The session authentication file """
from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User
from flask import (request, Blueprint, jsonify)
import os


class SessionAuth(Auth):
    """ the session authentication class """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create and return a session ID for user_id """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a user ID based on session ID """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the user with session ID in the cookie """
        s_id = self.session_cookie(request)
        u_id = self.user_id_for_session_id(s_id)
        return User.get(u_id)

    def destroy_session(self, request=None):
        """ destroys the user session """
        s_id = self.session_cookie(request)
        if not request or not s_id:
            return False
        u_id = self.user_id_for_session_id(s_id)
        if not u_id:
            return False
        del self.user_id_by_session_id[s_id]
        return True






















