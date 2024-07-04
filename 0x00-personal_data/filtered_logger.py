#!/usr/bin/env python3
"""
Module that defines a function `filter_datum`
"""
from typing import List
import re
import logging
import os
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("ssn", "password", "ip", "last_login", "user_agent")
PERSONAL_DATA_DB_NAME = "holberton"
PERSONAL_DATA_DB_USERNAME = "root"
PERSONAL_DATA_DB_PASSWORD = ""
PERSONAL_DATA_DB_HOST = "localhost"


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    fn that returns the log message obfuscated

    Args:
        fields: (List[str]) all fields obfuscated
        redaction: (str) what the field will obfuscated by
        message: (str) the log line
        separator: (str) the separator of the fields in the log line (message)

    Returns:
        (str) the obfuscated log message
    """
    def replace_field(match):
        """replace match"""
        field = match.group(1)
        if field in fields:
            return f"{field}={redaction}{separator}"
        return match.group(0)
    pattern = re.compile(rf"([^=]+)=([^{separator}]*){separator}")
    obfuscated_message = re.sub(pattern, replace_field, message)
    return obfuscated_message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, RedactingFormatter.REDACTION,
                            original_msg, RedactingFormatter.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # create streamHandler
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # add handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    return connector to database
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME") or PERSONAL_DATA_DB_USERNAME
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD") or PERSONAL_DATA_DB_PASSWORD
    host = os.getenv("PERSONAL_DATA_DB_HOST") or PERSONAL_DATA_DB_HOST
    database = os.getenv("PERSONAL_DATA_DB_NAME") or PERSONAL_DATA_DB_NAME
    return MySQLConnection(user=user, password=password, host=host, database=database)
