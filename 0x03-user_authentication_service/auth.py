#!/usr/bin/env python3
"""
auth.py
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
