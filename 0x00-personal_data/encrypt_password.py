#!/usr/bin/env python3
"""
This module enrypt passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password."""
    encode = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encode, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates the provided password matches the hashed password."""
    encoded = password.encode()
    return bcrypt.checkpw(encoded, hashed_password)
