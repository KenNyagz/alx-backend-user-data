#!/usr/bin/env python3
'''
Fetches obfuscated logs messages
'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    '''returns log message obfuscated'''
    pattern = '({})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)
