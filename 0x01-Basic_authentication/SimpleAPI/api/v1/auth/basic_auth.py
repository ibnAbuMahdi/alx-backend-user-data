#!/usr/bin/env python3
""" basic_auth """
from api.v1.auth.auth import Auth
from models.user import User
from typing import (Tuple, TypeVar)
import base64
import binascii


class BasicAuth(Auth):
    """ class for basic authentication """

    def extract_base64_authorization_header(self, a_header: str) -> str:
        """ extracts the base64 header """
        if not a_header or not isinstance(a_header, str) or \
                not a_header.startswith('Basic '):
            return None
        return a_header.split()[1]

    def decode_base64_authorization_header(self, b64_header: str) -> str:
        """ return the decoded @b64_header if valid b64 string """
        if not b64_header or not isinstance(b64_header, str):
            return None
        try:
            return base64.b64decode(b64_header).decode('utf-8')
        except (binascii.Error, ValueError) as e:
            return None

    def extract_user_credentials(self, d_b64_header: str) -> Tuple(str):
        """ return the credentials attached to the header
            authorization values
        """
        if not d_b64_header or not isinstance(d_b64_header, str) or \
                ':' not in d_b64_header:
            return None
        return d_b64_header.split(':')[0], \
            d_b64_header[d_b64_header.find(':')+1:]

    def user_object_from_credentials(self, email: str, pwd: str) \
            -> TypeVar('User'):
        """ create and return a User object from email and pwd """
        if not email or not isinstance(email, str) \
                or not pwd or not isinstance(pwd, str):
            return None
        users = User.search({'email': email})
        if not len(users) or not users[0].is_valid_password(pwd):
            return None
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the User instance based on Auth """
        a_header = self.authorization_header(request=request)
        if a_header:
            b64_header = \
                self.extract_base64_authorization_header(a_header=a_header)
            if b64_header:
                d_b64_header = \
                    self.decode_base64_authorization_header(b64_header)
                if d_b64_header:
                    user_creds = self.extract_user_credentials(d_b64_header)
                    if user_creds:
                        return self.user_object_from_credentials(user_creds)
