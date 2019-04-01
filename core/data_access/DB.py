import os
import sqlite3


class DB:

    def __init__(self):
        if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'production':
            self.filename = 'irs.db'
        else:
            self.filename = 'irs_dev.db'

    def __enter__(self):
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        self.conn.close()

    def query(self, *args):
        self.cur.execute(*args)
        return self.cur.fetchall()
