#!/usr/bin/env python3
""" Module of users views
"""
from api.v1.views import sess_views
from flask import abort, jsonify, request
from models.user import User
import os


@sess_views.route('/auth_session/login', methods=['POST'],
                  strict_slashes=False)
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


@sess_views.route('/auth_session/logout', methods=['DELETE'],
                  strict_slashes=False)
def logout():
    """ the logout method route """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
