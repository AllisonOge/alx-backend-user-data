#!/usr/bin/env python3
"""
Module for Auth class
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if path is None or excluded_paths is None or empty
        otherwise if path is in excluded_paths returns False
        """
        if path is None:
            return True
        if excluded_paths is None \
                or (isinstance(excluded_paths, list)
                    and len(excluded_paths) == 0):
            return True
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None if request is None or if request does not contain
        Authorization key in header otherwise return the value of the
        Authorization key in the header
        """
        if request is None:
            return
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """returns None"""
        return None
