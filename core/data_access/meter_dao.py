import core.models
from core.data_access.db import get_cursor as get_db


def find_by_id(id):
    with get_db() as db:
        db.execute("SELECT name, id FROM meters WHERE id = %s", (id,))
        record = db.fetchone()
    return core.models.Meter(record[0], record[1])

def insert(meter):
    with get_db() as db:
        db.execute("INSERT INTO meters (name) VALUES (%s) RETURNING id",
                    (meter.name))
        return db.fetchone()[0]

def delete(meter):
    with get_db() as db:
        db.execute("DELETE FROM meters WHERE id = %s", (meter._id,))
