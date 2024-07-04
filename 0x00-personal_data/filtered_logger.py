#!/usr/bin/env python3
"""
Module that defines a function `filter_datum`
"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
    def replace_field(match: re.Match):
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
        """format filtered record"""
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    return connector to database
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "holberton")
    return mysql.connector.connect(user=user,
                                   password=password, host=host,
                                   database=database)


def main() -> None:
    """read database and log filtered record to console"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")

    logger = get_logger()
    for row in cur:
        record = []
        for desc, entry in zip(cur.description, row):
            key_value = f"{desc[0]}={entry}"
            record.append(key_value)
        log = ";".join(record)
        logger.info(log)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
