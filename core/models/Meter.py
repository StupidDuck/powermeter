from datetime import datetime
from core.data_access import meter_dao

class Meter:

    def __init__(self, name, id=None):
        self.name = name
        self._id = id

    @staticmethod
    def find(_id):
        return meter_dao.find_by_id(_id)

    def save(self):
        self._id = meter_dao.insert(self)

    def delete(self):
        meter_dao.delete(self)
