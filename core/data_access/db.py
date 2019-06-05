import os
import psycopg2
from contextlib import contextmanager

DATABASE_URL = os.environ['DATABASE_URL']

@contextmanager
def get_cursor():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    yield connection.cursor()
    connection.commit()
    connection.close()

with get_cursor() as c:
    c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='users';""")
    if c.fetchone() is None:
        c.execute("""CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(30) NOT NULL
                        );""")
    c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='meters';""")
    if c.fetchone() is None:
        c.execute("""CREATE TABLE meters (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(30) NOT NULL,
                        user_id integer REFERENCES users (id)
                        );""")
    c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='indexes';""")
    if c.fetchone() is None:
        c.execute("""CREATE TABLE indexes (
                        id SERIAL PRIMARY KEY,
                        date DATE NOT NULL,
                        value REAL NOT NULL,
                        meter_id integer REFERENCES meters (id)
                        );""")
