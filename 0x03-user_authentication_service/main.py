#!/usr/bin/env python3
""" main module for testing end points of the app """
import requests
base_url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ tests for user registration """
    data = {"email": email, "password": password}
    r = requests.post(base_url+'/users', data=data)
    assert {"email": email, "message": "user created"} == r.json()
    assert r.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """ tests wrong user log in """
    data = {"email": email, "password": password}
    r = requests.post(base_url+'/sessions', data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ tests user log in """
    data = {"email": email, "password": password}
    r = requests.post(base_url+'/sessions', data=data)
    assert r.json() == {"email": email, "message": "logged in"}
    assert r.status_code == 200
    for c in r.cookies:
        if c.name == "session_id":
            return c.value


def profile_unlogged() -> None:
    """ tests get profile not logged in user """
    r = requests.get(base_url+'/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ tests profile of logged in user """
    r = requests.get(base_url+'/profile', cookies={'session_id': session_id})
    assert "email" in r.json()
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """ test user log out """
    r = requests.delete(base_url+'/sessions',
                        cookies={'session_id': session_id})
    assert r.json() == {"message": "Bienvenue"}
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    """ tests reset user password token """
    data = {"email": email}
    r = requests.post(base_url+'/reset_password', data=data)
    assert "email" in r.json() and "reset_token" in r.json()
    assert r.status_code == 200
    return r.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ tests update user password """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put(base_url+'/reset_password', data=data)
    assert r.json() == {"email": email, "message": "Password updated"}
    assert r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
