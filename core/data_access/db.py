import os
import sqlite3

FILENAME = os.environ['DB_FILENAME']
CONN = sqlite3.connect(FILENAME, check_same_thread=False)

def get_db():
    return CONN

def create_schema():
    with get_db() as db:
        db.execute("""CREATE TABLE indexes (
                     id integer primary key,
                     date  text,
                     value real);""")

def demo():
    with get_db() as db:
        db.execute("""INSERT INTO indexes (date, value) values
                     ('2018-11-13', 5146), ('2018-11-17', 5198), ('2018-11-18', 5208),
                     ('2018-11-20', 5231), ('2018-11-24', 5261), ('2018-12-07', 5391),
                     ('2018-12-09', 5408), ('2018-12-19', 5491), ('2018-12-27', 5559),
                     ('2019-01-11', 5729), ('2019-01-26', 5888), ('2019-02-08', 6015);""")

with CONN:
    STMT = CONN.execute(
        'SELECT name FROM sqlite_master WHERE type = ? AND name = ?;', ('table', 'indexes'))
    if STMT.fetchone() is None:
        create_schema()
        #demo()
