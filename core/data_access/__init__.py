from .db import get_cursor

with get_cursor() as c:
    c.execute("""CREATE TABLE IF NOT EXISTS meters (
                 id SERIAL PRIMARY KEY NOT NULL,
                 name TEXT NOT NULL,
                 user_id TEXT NOT NULL);""")
    c.execute("""CREATE TABLE IF NOT EXISTS indexes (
                 id SERIAL PRIMARY KEY NOT NULL,
                 date DATE NOT NULL,
                 value REAL NOT NULL,
                 meter_id INTEGER REFERENCES meters (id) ON DELETE CASCADE);""")
