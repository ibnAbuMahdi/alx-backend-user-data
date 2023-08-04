#!/usr/bin/env python3
""" filtered_logger """
from typing import (List, Sequence)
import re
import os
import mysql.connector
import logging
PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(f: List[str], red: str, msg: str, sep: str) -> str:
    """ returns an obfuscated message """
#    for f in fields:
    val: str = msg[msg.index(f[0])+len(f[0])+1:msg.find(sep, msg.index(f[0]))]
    msg = re.sub(val, red, msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__flds = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the log record message """
        m = filter_datum(self.__flds, self.REDACTION,
                         record.getMessage(), self.SEPARATOR)
        nr = logging.LogRecord(record.name, record.levelno, record.pathname,
                               record.lineno, m, record.args, record.exc_info)
        return super().format(nr)


def get_logger() -> logging.Logger:
    """ get logger function that uses RedactingFormatter """
    formatter: RedactedFormatter = RedactedFormatter(PII_FIELDS)
    logger: logging.Logger = logging.getLogger('user_data')
    handler: logging.StreamHandler = logging.streamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to MySQL database """
    host: str = os.environ["PERSONAL_DATA_DB_HOST"]
    user: str = os.environ["PERSONAL_DATA_DB_USERNAME"]
    password: str = os.environ["PERSONAL_DATA_DB_PASSWORD"]
    database: str = os.environ["PERSONAL_DATA_DB_NAME"]
    try:
        # Create a connection to the MySQL database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            return conn
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None


def main():
    """ the main method that returns formatted log from db """
    connection = get_db()
    fields = ("name", "email", "phone", "ssn", "password")
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in result:
            mes = "name={}; email={}; phone={}; ssn={}; password{}; ip={}; \
last_login={}; user_agent={}".\
                    format(row[0], row[1], row[2], row[3],
                           row[4], row[5], row[6], row[7])
            formatter: RedactingFormatter = RedactingFormatter(fields=fields)
            record = logging.LogRecord("user_data",
                                       logging.INFO, None, None,
                                       mes, None, None)
            print(formatter.format(record))


if __name__ == "__main__":
    main()
