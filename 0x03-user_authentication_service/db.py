#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Any
from sqlalchemy.pool import NullPool
from user import (Base, User)
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True,
                                     connect_args={"check_same_thread": False})
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, h_pwd: str) -> User:
        """ adds a user to db and return the user instance """
        if email and h_pwd:
            user: User = User(email=email,  hashed_password=h_pwd)
            self._session.add(user)
            self._session.commit()
            self._session.close()
            self._engine.dispose()
            return user
        return None

    def find_user_by(self, **kwargs) -> Any:
        """ returns a row in db based on @kwargs """
        usr = self._session.query(User).filter_by(**kwargs).one()
        self._session.close()
        return usr

    def update_user(self, u_id: int, **kwargs) -> None:
        """ updates a user and return None """
        user: User = self.find_user_by(id=u_id)
        sess = self._session
        for k in kwargs.keys():
            if k not in tuple(col.name for col in User.__table__.columns):
                raise ValueError

        for k, v in kwargs.items():
            setattr(user, k, v)
        sess.commit()
        sess.close()
