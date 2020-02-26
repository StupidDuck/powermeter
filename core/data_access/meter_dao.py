import core.models
from core.data_access.db import get_cursor as get_db


def find(user_id, _id=None):
    if _id is None:
        with get_db() as db:
            db.execute("""
                SELECT user_id, name, id FROM meters
                WHERE user_id = %s""", (user_id,))
            records = db.fetchall()
        return [core.models.Meter(record[0], record[1], record[2]) for record in records]
    else:
        with get_db() as db:
            db.execute("""
                SELECT user_id, name, id FROM meters
                WHERE user_id = %s AND id = %s""", (user_id, _id))
            record = db.fetchone()
            if record is None:
                return None
        return core.models.Meter(record[0], record[1], record[2])


def insert(meter):
    with get_db() as db:
        db.execute("INSERT INTO meters (user_id, name) VALUES (%s, %s) RETURNING id",
                    (meter.user_id, meter.name))
        return db.fetchone()[0]


def delete(meter):
    with get_db() as db:
        db.execute("DELETE FROM meters WHERE id = %s", (meter.id,))
