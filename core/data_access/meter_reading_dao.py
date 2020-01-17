import core.models
from core.data_access.db import get_cursor as get_db


def find(user_id, id):
    if id is None:
        with get_db() as db:
            db.execute("""
                SELECT indexes.date, indexes.value, indexes.meter_id, indexes.id
                FROM indexes INNER JOIN meters ON indexes.meter_id = meters.id
                WHERE meters.user_id = %s""", (user_id,))
            records = db.fetchall()
        return [core.models.MeterReading(record[0], record[1], record[2], record[3]) for record in records]
    else:
        with get_db() as db:
            db.execute("""
                SELECT indexes.date, indexes.value, indexes.meter_id, indexes.id
                FROM indexes INNER JOIN meters ON indexes.meter_id = meters.id
                WHERE meters.user_id = %s AND indexes.id = %s""", (user_id, id,))
            record = db.fetchone()
            if record is None:
                return None
        return core.models.MeterReading(record[0], record[1], record[2], record[3])

def insert(meter_reading):
    with get_db() as db:
        db.execute("INSERT INTO indexes (date, value, meter_id) VALUES (%s, %s, %s) RETURNING id",
                    (meter_reading.date, meter_reading.value, meter_reading.meter_id))
        return db.fetchone()[0]

def delete(meter_reading):
    with get_db() as db:
        db.execute("DELETE FROM indexes WHERE id = %s", (meter_reading._id,))
