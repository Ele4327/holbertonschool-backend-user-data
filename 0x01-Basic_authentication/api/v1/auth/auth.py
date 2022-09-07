#!/usr/bin/env python3
"""
    Manage API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class to manage API requests"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Test """
        if path is None or not excluded_paths:
            return True
        for x in excluded_paths:
            if x.endswith('*') and path.startswith(x[:-1]):
                return False
            elif x in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Test """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Test """
        return None
