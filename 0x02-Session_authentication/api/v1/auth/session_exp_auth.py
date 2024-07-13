#!/usr/bin/env python3
"""
Module for Session Authentication with expiration time
"""
from os import getenv
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Authentication with expiration"""
    def __init__(self):
        """initialization"""
        self.session_duration = getenv("SESSION_DURATION", 0)
        try:
            self.session_duration = int(self.session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session id from user id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return
        SessionAuth.user_id_by_session_id.update({
                                session_id: {"user_id": user_id,
                                             "created_at": datetime.now()}})
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """return user id given the session id"""
        if session_id is None:
            return
        session = SessionAuth.user_id_by_session_id.get(session_id)
        if session is None:
            return
        if session.get("user_id") is None:
            return
        if self.session_duration <= 0:
            return user_id
        created_at = session.get("created_at")
        if created_at is None:
            return
        expiration_date = created_at + \
            timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return
        return session.get("user_id")
