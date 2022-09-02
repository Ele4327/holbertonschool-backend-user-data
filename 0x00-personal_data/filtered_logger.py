#!/usr/bin/env python3
"""
    Write a function that returns the
    log message obfuscated
"""

from typing import List
import re
import logging
import mysql.connector
from os import environ

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def main():
    """
        Function that takes no arguments and returns nothing
        The function will obtain a database connection using
        get_db and retrieve all rows in the users table and
        display each row under a filtered format

        Filtered fields:
        name
        email
        phone
        ssn
        password
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users;')
    rows = cursor.fetchall()

    logger = get_logger()
    field_names = [i[0] for i in cursor.description]

    for row in rows:
        message = ''
        for field in range(len(row)):
            message += f'{field_names[field]}={row[field]};'
        logger.info(message)

    cursor.close()
    db.close()


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


def get_logger() -> logging.Logger:
    """ Return a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.basicConfig(format=RedactingFormatter.FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database object"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    return (mysql.connector.connection.MySQLConnection(user=username,
                                                       password=password,
                                                       host=host,
                                                       database=db_name))


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            Filter values in incoming log records using filter_datum
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
