from core.data_access import meter_dao


class Meter:

    def __init__(self, user_id, name, meter_id=None):
        self._user_id = user_id
        self.name = name
        self._id = meter_id

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    def save(self):
        self._id = meter_dao.insert(self)

    def delete(self):
        return meter_dao.delete(self)

    @staticmethod
    def find(user_id):
        return meter_dao.find(user_id)
