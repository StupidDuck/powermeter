import os
import psycopg2
from contextlib import contextmanager

DATABASE_URL = os.environ['DATABASE_URL']

@contextmanager
def get_cursor():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    yield connection.cursor()
    connection.close()

with get_cursor() as c:
    stmt = c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='indexes';""")
    if stmt.fetchone() is None:
        c.execute("""CREATE TABLE indexes (
                        id serial,
                        date  date,
                        value real,
                        PRIMARY KEY(id);""")
