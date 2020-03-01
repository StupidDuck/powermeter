from core.data_access import index_dao


class Index:

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

    def save(self):
        self._id = index_dao.insert(self)

    def delete(self):
        return index_dao.delete(self)

    @staticmethod
    def find(user_id, meter_id):
        return index_dao.find(user_id, meter_id)