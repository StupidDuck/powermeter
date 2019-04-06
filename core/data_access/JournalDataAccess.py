import core.models
from core.data_access.DB import DB


class JournalDataAccess:

    @classmethod
    def find_all(cls):
        with DB() as db:
            records = db.query("SELECT date, value, id FROM indexes ORDER BY date")

        return [core.models.MeterReading.MeterReading(record[0], record[1], record[2]) for record in records]
