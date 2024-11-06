#!/usr/bin/env python3
"""
"""
import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated"""
    for i in fields:
        message = re.sub(
                        f'{i}=.*?{separator}',
                        f'{i}={redaction}{separator}',
                        message
                        )
    return message
