from core.data_access.MeterReadingDataAccess import MeterReadingDataAccess


class MeterReading:

    def __init__(self, date, value, id=None):
        self.check_date_format(date)
        self.id = id
        self.date = date
        self.value = value

    def __str__(self):
        return "date: {}, value : {}, days : {}, mean_consumption_per_day : {}".format(self.date, self.value, self.days, self.mean_consumption_per_day)

    @staticmethod
    def get_by_id(id):
        mr = MeterReadingDataAccess.find_by_id(id)
        if len(mr) > 0:
            return mr[0]
        return None

    def create(self):
        MeterReadingDataAccess.insert([self])

    def delete(self):
        MeterReadingDataAccess.delete([self])

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
