#!/usr/bin/env python3
""" filtered_logger """
from typing import (List, Union, Sequence)
import re
import os
import mysql.connector
import logging
PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns an obfuscated message """
    for f in fields:
        val: str = message[message.index(f)+len(f)+1:
                           message.find(separator, message.index(f))]
        message = re.sub(re.escape(val), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for Formatting records
        """

    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s %(levelname)s \
%(asctime)-15s: %(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]) -> None:
        """ the init class method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the log record message """
        m: str = filter_datum(self.__fields, self.REDACTION,
                              record.getMessage(), self.SEPARATOR)
        nr: logging.LogRecord = logging.LogRecord(record.name,
                                                  record.levelno,
                                                  record.pathname,
                                                  record.lineno, m,
                                                  record.args,
                                                  record.exc_info)
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


def get_db() -> Union[mysql.connector.connection.MySQLConnection, None]:
    """ returns a connector to MySQL database """
    host: str = os.environ["PERSONAL_DATA_DB_HOST"]
    user: str = os.environ["PERSONAL_DATA_DB_USERNAME"]
    password: str = os.environ["PERSONAL_DATA_DB_PASSWORD"]
    database: str = os.environ["PERSONAL_DATA_DB_NAME"]
    try:
        # Create a connection to the MySQL database
        conn: mysql.connector.connection.MySQLConnection = mysql.\
            connector.connect(
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
    connection: Union[mysql.connector.connection.MySQLConnection, None]\
        = get_db()
    fields: Sequence = ("name", "email", "phone", "ssn", "password")
    if connection is not None:
        cursor: Any = connection.cursor()
        cursor.execute("SELECT * FROM users")
        result: List = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in result:
            mes: str = "name={}; email={}; phone={}; ssn={}; password{};\
                    ip={}; last_login={}; user_agent={}".\
                    format(row[0], row[1], row[2], row[3],
                           row[4], row[5], row[6], row[7])
            formatter: RedactingFormatter = RedactingFormatter(fields=fields)
            record: logging.LogRecord = logging.LogRecord("user_data",
                                                          logging.INFO, None,
                                                          None, mes, None,
                                                          None)
            print(formatter.format(record))


if __name__ == "__main__":
    main()
