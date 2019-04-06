import core.models
from core.data_access.DB import DB


class MeterReadingDataAccess:

    @classmethod
    def find_by_id(cls, id):
        with DB() as db:
            records = db.query("SELECT date, value, id FROM indexes WHERE id = ?", (id,))

        if len(records) == 1:
            return core.models.MeterReading.MeterReading(records[0][0], records[0][1], records[0][2])
        else:
            return None

    @classmethod
    def insert(cls, meter_reading):
        with DB() as db:
            db.query("INSERT INTO indexes (date, value) VALUES (?, ?)", (meter_reading.date, meter_reading.value))

    @classmethod
    def delete(cls, meter_reading):
        with DB() as db:
            db.query("DELETE FROM indexes WHERE id = ?", (meter_reading.id,))
