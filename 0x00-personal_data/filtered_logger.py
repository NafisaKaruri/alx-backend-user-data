#!/usr/bin/env python3
"""
This module provides utilities for logging user data while redacting sensitive
Personally Identifiable Information (PII) and securely hashing passwords.
"""
import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                        f'{i}={redaction}{separator}', message)
    return message
