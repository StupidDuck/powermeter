import core.model
from core.data_access.db import get_cursor as get_db


def find(user_id):
    with get_db() as db:
        db.execute("""
            SELECT user_id, name, id FROM meters
            WHERE user_id = %s;""", (user_id,))
        records = db.fetchall()
        if records is None:
            return None
    return [core.model.Meter(record[0], record[1], record[2]) for record in records]


def insert(meter):
    with get_db() as db:
        db.execute("INSERT INTO meters (user_id, name) VALUES (%s, %s) RETURNING id;",
                   (meter.user_id, meter.name))
        # db.execute("SELECT last_insert_rowid();")
        if record := db.fetchone():
            return record[0]
        return None


def delete(meter):
    with get_db() as db:
        db.execute("DELETE FROM meters WHERE id = %s;", (meter.id,))
        return meter.id
