import core.models
from core.data_access.DB import conn


class JournalDataAccess:

    @classmethod
    def find_all(cls):
        with conn:
            stmt = conn.execute("SELECT date, value, id FROM indexes ORDER BY date")
            records = stmt.fetchall()

        return [core.models.MeterReading.MeterReading(record[0], record[1], record[2]) for record in records]
