#!/usr/bin/env python3
"""
Module to encrypt password
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    hash a password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
