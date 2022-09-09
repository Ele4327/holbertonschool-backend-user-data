#!/usr/bin/env python3
"""
    Session auth
"""

import uuid
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Class Session auth """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a sessionID for user """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID on based on sessions ID """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
