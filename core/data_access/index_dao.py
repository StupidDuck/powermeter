import core.model
from core.data_access.db_sqlite import get_cursor as get_db


def find(user_id, meter_id):
    with get_db() as db:
        db.execute("""
            SELECT indexes.date, indexes.value, indexes.meter_id, indexes.id
            FROM indexes INNER JOIN meters ON indexes.meter_id = meters.id
            WHERE meters.user_id = ? AND indexes.meter_id = ?;""", (user_id, meter_id))
        records = db.fetchall()
        if records is None:
            return None
    return [core.model.Index(record[0], record[1], record[2], record[3]) for record in records]


def insert(meter_reading):
    with get_db() as db:
        db.execute("INSERT INTO indexes (date, value, meter_id) VALUES (?, ?, ?);",
                   (meter_reading.date, meter_reading.value, meter_reading.meter_id))
        db.execute("SELECT last_insert_rowid();")
        if record := db.fetchone():
            return record[0]
        return None


def delete(meter_reading):
    with get_db() as db:
        db.execute("DELETE FROM indexes WHERE id = ?;", (meter_reading.id,))
        return meter_reading.id
