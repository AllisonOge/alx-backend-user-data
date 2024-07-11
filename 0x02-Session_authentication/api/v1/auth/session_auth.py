#!/usr/bin/env python3
"""
Module for the SessionAuth class
"""
from typing import TypeVar
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """class for creating a session authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a `user_id`."""
        if user_id is None:
            return
        if not isinstance(user_id, str):
            return
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a `User` ID based on a `Session` ID"""
        if session_id is None:
            return
        if not isinstance(session_id, str):
            return
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) \
            -> TypeVar("User"):  # an overload function
        """returns a `User` instance based on a cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        if user_id is None:
            return
        return User.get(user_id)
