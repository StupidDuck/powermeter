from core.model import Meter


class MeterViewModel:
    def __init__(self, user_id):
        self._user_id = user_id
        self._meters = Meter.find(user_id=user_id)

    @property
    def user_id(self):
        return self._user_id

    def get(self):
        return [{
            'id': meter.id,
            'name': meter.name
        } for meter in self._meters]

    def save(self, name):
        _meter = Meter(user_id=self._user_id, name=name)
        _meter.save()
        return _meter.id

    def delete(self, meter_id):
        try:
            _meter = [meter for meter in self._meters if meter.id == meter_id][0]
            return _meter.delete()
        except IndexError:
            return None
