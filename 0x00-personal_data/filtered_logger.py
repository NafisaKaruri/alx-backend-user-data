#!/usr/bin/env python3
"""
This module provides utilities for logging user data while redacting sensitive
Personally Identifiable Information (PII) and securely hashing passwords.
"""
from typing import List
from os import environ
import logging
import mysql.connector
import re

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format"""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, ';')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    db_username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connection.MySQLConnection(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
    return connector


def get_logger() -> logging.Logger:
    """Returns theh logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message
