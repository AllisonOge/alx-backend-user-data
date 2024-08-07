#!/usr/bin/env python3
"""
auth.py
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
