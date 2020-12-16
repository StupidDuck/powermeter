from core.model import Index, Meter, Journal


class JournalViewModel:
    def __init__(self, user_id, meter_id):
        self._meters = Meter.find(user_id)
        self._meter = [meter for meter in self._meters if meter.id == meter_id][0]
        self._indexes = Index.find(user_id=user_id, meter_id=meter_id)
        self._journal = Journal(self._indexes)

    def get(self, days=15):
        return {
            'meter_id': self._meter.id,
            'meter_name': self._meter.name,
            'entries': [{
                'id': index.id,
                'date': index.date,
                'value': index.value,
                'mean_consumption_per_day': index.mean_consumption_per_day,
                'duration': index.days
            } for index in self._journal],
            'mean': self._journal.mean,
            'days': days,
            'trend_last_days': self._journal.trend_last_days(days)
        }

    def save_index(self, value, date):
        _index = Index(date, value, self._meter.id)
        _index.save()
        return _index.id

    def delete_index(self, index_id):
        try:
            _index = [index for index in self._indexes if index.id == index_id][0]
            return _index.delete()
        except IndexError:
            return None

    def export_csv(self):
        path = "export.csv"
        with open(path, mode="w", encoding="UTF-8") as file:
            for mr in self._indexes:
                file.write("{},{}\n".format(mr.date, mr.value))
        return path

    def import_csv(self, file):
        line = file.readline().decode("utf-8")
        while line:
            line_list = line.split(',')
            date = line_list[0]
            value = line_list[1].strip('\n')
            # meter_reading_dao.insert(core.model.MeterReading(date, value, self._meter_id))
            self.save_index(value, date)
            line = file.readline().decode("utf-8")
