from datetime import datetime
from core.data_access import meter_reading_dao

class MeterReading:

    def __init__(self, date, value, mr_id=None):
        self.check_date_format(date)
        self._id = mr_id
        self.date = date
        self.value = value
        self.days = 0
        self.consumption = 0

    def __str__(self):
        return "date: {}, value : {}, days : {}, mean_consumption_per_day : {}".format(
            self.date, self.value, self.days, self.mean_consumption_per_day)

    @staticmethod
    def find(mr_id):
        return meter_reading_dao.find_by_id(mr_id)

    def save(self):
        self._id = meter_reading_dao.insert(self)

    def delete(self):
        meter_reading_dao.delete(self)

    @property
    def mean_consumption_per_day(self):
        mean = 0
        if self.days > 0:
            mean = self.consumption / self.days

        return float("{0:.2f}".format(mean))

    @staticmethod
    def check_date_format(date):
        if not isinstance(date, str):
            raise TypeError('The date must be a string like YYYY-MM-DD')
        try:
            datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('The date must be a string like YYYY-MM-DD')
