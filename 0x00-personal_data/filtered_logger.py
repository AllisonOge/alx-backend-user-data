#!/usr/bin/env python3
"""
Module that defines a function `filter_datum`
"""
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str):
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
    all_fields = {
            k: v for k, v in list(map(lambda x: x.split("="), message.split(separator)[:-1]))
            }
    for field in fields:
        if field not in all_fields:
            return
        all_fields[field] = redaction
    return ";".join(f"{k}={v}" for k, v in all_fields.items()) + ";"
