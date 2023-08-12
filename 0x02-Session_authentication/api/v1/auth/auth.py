#!/usr/bin/env python3
""" The authentication handling file"""
from flask import request
from typing import (List, TypeVar)
import os


class Auth:
    """Class to handle authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determine if path requires auth"""
        if path is None or excluded_paths is None:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.endswith('*'):
                if path.startswith(ex_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns the authorization header in the request"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the current user based on details in request """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        session_name = os.getenv('SESSION_NAME')
        if not request:
            return None
        return request.cookies.get(session_name)
