import core.models
from core.data_access.db import get_cursor as get_db


def find_all():
    with get_db() as db:
        db.execute("SELECT date, value, id FROM indexes ORDER BY date")
        records = db.fetchall()

    return [core.models.MeterReading(record[0], record[1], record[2]) for record in records]
