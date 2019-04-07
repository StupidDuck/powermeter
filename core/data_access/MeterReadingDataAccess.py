import core.models
from core.data_access.DB import conn


class MeterReadingDataAccess:

    @classmethod
    def find_by_id(cls, id):
        with conn:
            stmt = db.execute("SELECT date, value, id FROM indexes WHERE id = ?", (id,))
            record = stmt.fetchone()
        return core.models.MeterReading.MeterReading(record[0], record[1], record[2])

    @classmethod
    def insert(cls, meter_reading):
        with conn:
            cursor = conn.execute("INSERT INTO indexes (date, value) VALUES (?, ?)", (meter_reading.date, meter_reading.value))
            return cursor.lastrowid

    @classmethod
    def delete(cls, meter_reading):
        with conn:
            conn.execute("DELETE FROM indexes WHERE id = ?", (meter_reading.id,))
