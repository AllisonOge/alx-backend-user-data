#!/usr/bin/env python3
"""
Basic Authentication class
"""
from .auth import Auth
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
