from datetime import datetime
from core.data_access import meter_dao

class Meter:

    def __init__(self, user_id, name, id=None):
        self.user_id = user_id
        self.name = name
        self._id = id

    @staticmethod
    def find(_id):
        return meter_dao.find_by_id(_id)

    @staticmethod
    def find_all(user_id):
        return meter_dao.find_all(user_id)

    def save(self):
        self._id = meter_dao.insert(self)

    def delete(self):
        meter_dao.delete(self)
