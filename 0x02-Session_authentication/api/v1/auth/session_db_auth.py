#!/usr/bin/env python3
""" The session (with expiration and db) authentication file """
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import (datetime, timedelta)
from typing import TypeVar
from models.user import User
from models.user_session import UserSession
from flask import (request, Blueprint, jsonify)
import os


class SessionDBAuth(SessionExpAuth):
    """ the session with Expiration and db authentication class """

    def create_session(self, user_id: str = None) -> str:
        """ create and return a session ID for user_id """
        s_id = super().create_session(user_id)
        if not s_id:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[s_id] = session_dict
        user_session = UserSession(user_id=user_id, session_id=s_id)
        user_session.save()
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ create and return a session ID for user_id """
        if not session_id or session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        exp_time = self.user_id_by_session_id[session_id]['created_at']\
            + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        users = UserSession.search({'session_id': session_id})
        return users[0].user_id

    def destroy_session(self, request=None):
        """ destroy the user session """
        s_id = self.session_cookie(request)
        if not request or not s_id:
            return False
        u_id = self.user_id_for_session_id(s_id)
        if not u_id:
            return False
        del self.user_id_by_session_id[s_id]
        users = UserSession.search({'session_id': s_id})
        users[0].remove()
        return True
