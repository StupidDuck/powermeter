import os
import sqlite3
from contextlib import contextmanager


DATABASE_FILENAME = os.environ['DATABASE_FILENAME']


@contextmanager
def get_cursor():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_FILENAME)
        yield connection.cursor()
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error in SQLITE3 : ${e}")
    finally:
        if connection is not None:
            connection.close()
