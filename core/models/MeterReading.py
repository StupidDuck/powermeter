from core.data_access import meter_reading_dao


class MeterReading:

    def __init__(self, date, value, meter_id, _id=None):
        self._id = _id
        self.date = date
        self.value = value
        self.meter_id = meter_id
        self.days = 0
        self.consumption = 0

    @property
    def id(self):
        return self._id

    @property
    def mean_consumption_per_day(self):
        mean = 0
        if self.days > 0:
            mean = self.consumption / self.days

        return float("{0:.2f}".format(mean))

    @staticmethod
    def find(**kwargs):
        if '_id' in kwargs:
            return meter_reading_dao.find(kwargs['user_id'], kwargs['_id'])
        else:
            return meter_reading_dao.find(kwargs['user_id'])

    def save(self):
        self._id = meter_reading_dao.insert(self)

    def delete(self):
        meter_reading_dao.delete(self)
