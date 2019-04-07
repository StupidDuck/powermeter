import os
import sqlite3

filename = 'irs_dev.db'
if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'production':
    filename = 'irs.db'

conn = sqlite3.connect(filename, check_same_thread=False)

with conn:
    stmt = conn.execute('SELECT name FROM sqlite_master WHERE type = ? AND name = ?;', ('table', 'indexes'))
    if (stmt.fetchone()) == None:
        create_schema()
        #demo()

def create_schema():
  with conn:
      conn.execute("""CREATE TABLE indexes (
                  id integer primary key,
                  date  text,
                  value real);""")

def demo():
    with conn:
      conn.execute("""INSERT INTO indexes (date, value) values
                      ('2018-11-13', 5146), ('2018-11-17', 5198), ('2018-11-18', 5208),
                      ('2018-11-20', 5231), ('2018-11-24', 5261), ('2018-12-07', 5391),
                      ('2018-12-09', 5408), ('2018-12-19', 5491), ('2018-12-27', 5559),
                      ('2019-01-11', 5729), ('2019-01-26', 5888), ('2019-02-08', 6015);""")
