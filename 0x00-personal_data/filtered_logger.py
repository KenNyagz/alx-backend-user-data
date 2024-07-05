#!/usr/bin/env python3
'''
Fetches obfuscated logs messages
'''
import os
import re
import logging
import mysql.connector
from mysql.connector import connection, Error
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        message = super(RedactingFormatter, self).format(record)
        record_msg = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return record_msg
        # return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    '''returns log message obfuscated'''
    pattern = '({})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)


def get_logger() -> logging.Logger:
    '''returns a logger object named 'user_data' set to log up to INFO level'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''connects to a database and returns the connection object'''
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return db_conn


def main() -> None:
    '''entry point'''
    logger = get_logger()
    db = get_db()
    cur = db.cursor()
    query = "SELECT * FROM users;"
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        message = ("name={}; email={}; phone={}; ssn={}; password={}; "
                   "ip={}; last_login={}; user_agent={};").format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(message)
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
