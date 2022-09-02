#!/usr/bin/env python3
"""
    Write a function that returns the
    log message obfuscated
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
        The function should use a regex
        to replace occurrences of certain field values.
        filter_datum should be less than 5 lines long
        and use re.sub to perform the substitution with a single regex.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message
