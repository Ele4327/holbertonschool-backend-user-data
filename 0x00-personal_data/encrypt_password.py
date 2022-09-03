#!/usr/bin/env python3
"""
    Encrypt Password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
        Implement a hash_password function
        that expects one string argument
        name password and returns a salted,
        hashed password, which is a byte string.
    """
    return (bcrypt.hashpw(bytes(password.encode(), bcrypt.gensalt())))
