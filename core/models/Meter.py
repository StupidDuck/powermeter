from datetime import datetime
from core.data_access import meter_dao


class Meter:

    def __init__(self, user_id, name, _id=None):
        self._id = _id
        self.user_id = user_id
        self.name = name

    @property
    def id(self):
        return self._id

    @staticmethod
    def find(**kwargs):
        if '_id' in kwargs:
            return meter_dao.find(kwargs['user_id'], kwargs['_id'])
        else:
            return meter_dao.find(kwargs['user_id'])

    def save(self):
        self._id = meter_dao.insert(self)

    def delete(self):
        meter_dao.delete(self)
