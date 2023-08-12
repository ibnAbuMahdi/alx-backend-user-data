#!/usr/bin/env python3
""" A user session model """
from models.base import Base


class UserSession(Base):
    """ The user session class """

    def __init__(self, *args: list, **kwargs: dict):
        """ initializes the user_id and session_id """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

