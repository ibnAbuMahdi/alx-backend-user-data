#!/usr/bin/env python3
""" basic_auth """
from api.v1.auth.auth import Auth
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

