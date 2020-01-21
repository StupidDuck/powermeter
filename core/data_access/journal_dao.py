import core.models
from core.data_access.db import get_cursor as get_db


def find_all(meter_id):
    with get_db() as db:
        db.execute("""
            SELECT date, value, meter_id, id
            FROM indexes
            WHERE meter_id = %s ORDER BY date""", (meter_id,))
        records = db.fetchall()

    return [core.models.MeterReading(record[0], record[1], record[2], record[3]) for record in records]
