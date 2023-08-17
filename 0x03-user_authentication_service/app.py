#!/usr/bin/env python3
""" The flask app """
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
app: Flask = Flask(__name__)
AUTH: Auth = Auth()


@app.route('/', methods=['GET'])
def index():
    """ index route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ handles new user registration """
    email = request.form.get('email')
    pwd = request.form.get('password')

    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as e:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ handles new user login """
    email: str = request.form.get('email')
    pwd: str = request.form.get('password')

    if not AUTH.valid_login(email, pwd):
        abort(401)
    else:
        s_id: str = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", s_id)
        return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout a user and delete session """
    s_id = request.cookies.get('session_id')
    found = AUTH.get_user_from_session_id(s_id)
    if found:
        AUTH.destroy_session(found.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ returns the user profile if exist """
    s_id = request.cookies.get('session_id')
    found = AUTH.get_user_from_session_id(s_id)
    if found:
        return jsonify({"email": found.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ generate and return a reset password token """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError as e:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ updates a user password """
    email = request.form.get('email')
    r_tkn = request.form.get('reset_token')
    n_pwd = request.form.get('new_password')
    try:
        AUTH.update_password(r_tkn, n_pwd)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
