import os
from contextlib import contextmanager
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


@contextmanager
def get_cursor():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    yield connection.cursor()
    connection.commit()
    connection.close()
