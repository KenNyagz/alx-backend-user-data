#!/usr/bin/env python3
'''
Fetches obfuscated logs messages
'''
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''contructor method'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''method that handles the log formatting'''
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    '''returns log message obfuscated'''
    pattern = '({})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)
