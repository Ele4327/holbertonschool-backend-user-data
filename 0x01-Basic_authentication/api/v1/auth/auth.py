#!/usr/bin/env python3
"""
    Manage API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """  """
        return False

    def authorization_header(self, request=None) -> str:
        """ """
        return None
