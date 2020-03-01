from .db_sqlite import get_cursor

with get_cursor() as c:
    c.execute("""CREATE TABLE IF NOT EXISTS meters (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 user_id TEXT NOT NULL);""")
    c.execute("""CREATE TABLE IF NOT EXISTS indexes (
                 id INTEGER PRIMARY KEY,
                 date TEXT NOT NULL,
                 value REAL NOT NULL,
                 meter_id INTEGER REFERENCES meters (id) ON DELETE CASCADE);""")
