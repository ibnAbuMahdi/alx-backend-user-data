#!/usr/bin/env python3
""" The session (with expiration) authentication file """
from api.v1.auth.session_auth import SessionAuth
from datetime import (datetime, timedelta)
from typing import TypeVar
from models.user import User
from flask import (request, Blueprint, jsonify)
import os


class SessionExpAuth(SessionAuth):
    """ the session with Expiration authentication class """

    def __init__(self):
        """ init the instance """
        
        s_drtn = os.getenv('SESSION_DURATION')
        if not s_drtn or not s_drtn.isdigit():
            self.session_duration = 0
            return
        self.session_duration = int(s_drtn)

    def create_session(self, user_id: str = None) -> str:
        """ create and return a session ID for user_id """
        s_id = super().create_session(user_id)
        if not s_id:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[s_id] = session_dict
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
        return self.user_id_by_session_id[session_id]['user_id']


