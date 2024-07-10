#!/usr/bin/env python3
"""
Basic Authentication class
"""
from typing import TypeVar
from .auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic Authentication class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if not authorization_header.startswith("Basic "):
            return
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            decoded_string = \
                    base64.b64decode(base64_authorization_header)
            return decoded_string.decode("utf-8")
        except:  # noqa
            pass
        return

    def extract_user_credentials(self,
                                 decode_base64_authorization_header:
                                 str) -> (str, str):
        """return the user email and password from the Base64 decoded value"""
        if decode_base64_authorization_header is None:
            return None, None
        if not isinstance(decode_base64_authorization_header, str):
            return None, None
        if ":" not in decode_base64_authorization_header:
            return None, None
        return decode_base64_authorization_header.split(":")

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar("User"):
        """returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return
        if user_pwd is None or not isinstance(user_pwd, str):
            return
        searches = User.search(dict(email=user_email))
        if len(searches) == 0:
            return
        user = searches[0]
        if not user.is_valid_password(user_pwd):
            return
        return user
