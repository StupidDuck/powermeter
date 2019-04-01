from db import DB
import os
import uuid
import hashlib


def create_indexes():
  with DB() as db:
      db.query("""CREATE TABLE indexes (
                  id integer primary key,
                  date  text,
                  value real);""")

def demo_indexes():
    with DB() as db:
      db.query("""INSERT INTO indexes (date, value) values
                      ('2018-11-13', 5146), ('2018-11-17', 5198), ('2018-11-18', 5208),
                      ('2018-11-20', 5231), ('2018-11-24', 5261), ('2018-12-07', 5391),
                      ('2018-12-09', 5408), ('2018-12-19', 5491), ('2018-12-27', 5559),
                      ('2019-01-11', 5729), ('2019-01-26', 5888), ('2019-02-08', 6015);""")
