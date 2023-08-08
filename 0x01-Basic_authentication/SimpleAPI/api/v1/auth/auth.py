#!/usr/bin/env python3
""" The authentication handling file"""
from flask import request
from typing import (List, TypeVar)

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
    

    def authorization_header(self, request=None) -> str:
        """ returns the authorization header in the request"""
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the current user based on details in request """
        return None