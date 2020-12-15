import os
from contextlib import contextmanager

if os.environ['FLASK_ENV'] == 'production':
    import psycopg2
    DATABASE_URL = os.environ['DATABASE_URL']

    @contextmanager
    def get_cursor():
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        yield connection.cursor()
        connection.commit()
        connection.close()

elif os.environ['FLASK_ENV'] == 'development':
    import sqlite3
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
