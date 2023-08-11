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


sess_views = Blueprint("sess_views", __name__, url_prefix="/api/v1")
@sess_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_session():
    """ login into a user session or create new session """
    email = request.form.get('email')
    pword = request.form.get('password')

    if not email:
        return jsonify({'error': 'email missing'}), 400

    if not pword:
        return jsonify({'error': 'password missing'}), 400
    
    users = User.search({'email': email})
    if not len(users):
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(pword):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    s_id = auth.create_session(users[0].id)
    resp = jsonify(users[0].to_json())
    resp.set_cookie(os.getenv('SESSION_NAME'), s_id)
    return resp
