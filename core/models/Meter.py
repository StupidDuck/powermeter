from datetime import datetime
from core.data_access import meter_dao


class Meter:

    def __init__(self, user_id, name, id=None):
        self._id = id
        self.user_id = user_id
        self.name = name

    @staticmethod
    def find(**kwargs):
        if 'id' in kwargs:
            return meter_dao.find(kwargs['user_id'], kwargs['id'])
        else:
            return meter_dao.find(kwargs['user_id'], id=None)

    def save(self):
        self._id = meter_dao.insert(self)

    def delete(self):
        meter_dao.delete(self)
