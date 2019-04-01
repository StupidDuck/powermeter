#from typing import List
import core.models
from core.data_access.DB import DB

class MeterReadingDataAccess:

    @classmethod
    def find_all(cls):
        with DB() as db:
            records = db.query("SELECT date, value, id FROM indexes ORDER BY date")

        return [core.models.MeterReading.MeterReading(record[0], record[1], record[2]) for record in records]

    @classmethod
    def find_by_id(cls, id):
        with DB() as db:
            records = db.query("SELECT date, value, id FROM indexes WHERE id = ?", (id,))

        return [core.models.MeterReading.MeterReading(record[0], record[1], record[2]) for record in records]


    @classmethod
    #def insert(cls, meter_readings: List[MeterReading]):
    def insert(cls, meter_readings):
        with DB() as db:
            for meter_reading in meter_readings:
                db.query("INSERT INTO indexes (date, value) VALUES (?, ?)", (meter_reading.date, meter_reading.value))

    @classmethod
    #def delete(cls, meter_readings: List[MeterReading]):
    def delete(cls, meter_readings):
        with DB() as db:
            for meter_reading in meter_readings:
                db.query("DELETE FROM indexes WHERE id = ?", (meter_reading.id,))
