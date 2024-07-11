#!/usr/bin/env python3
"""
Module for the SessionAuth class
"""
from .auth import Auth
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
        session_id = uuid.uuid4()
        SessionAuth.user_id_by_session_id.update({f'{session_id}': user_id})
        return session_id
