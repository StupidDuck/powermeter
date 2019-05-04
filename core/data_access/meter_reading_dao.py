import core.models
from core.data_access.db import get_cursor as get_db


def find_by_id(mr_id):
    with get_db() as db:
        stmt = db.execute("SELECT date, value, id FROM indexes WHERE id = ?", (mr_id,))
        record = stmt.fetchone()
    return core.models.MeterReading(record[0], record[1], record[2])

def insert(meter_reading):
    with get_db() as db:
        db.execute("INSERT INTO indexes (date, value) VALUES (?, ?) RETURNING id",
                    (meter_reading.date, meter_reading.value))
        return db.fetchone()[0]

def delete(meter_reading):
    with get_db() as db:
        db.execute("DELETE FROM indexes WHERE id = ?", (meter_reading.id,))
