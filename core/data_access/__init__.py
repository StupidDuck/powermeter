from .db import get_cursor

with get_cursor() as c:
    c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='meters';""")
    if c.fetchone() is None:
        c.execute("""CREATE TABLE meters (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(30) NOT NULL,
                        user_id text NOT NULL
                        );""")
    c.execute("""SELECT table_name
                        FROM information_schema.tables
                        WHERE table_name='indexes';""")
    if c.fetchone() is None:
        c.execute("""CREATE TABLE indexes (
                        id SERIAL PRIMARY KEY,
                        date DATE NOT NULL,
                        value REAL NOT NULL,
                        meter_id integer REFERENCES meters (id) ON DELETE CASCADE
                        );""")
