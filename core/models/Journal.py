from datetime import datetime
import core.models
from core.data_access import journal_dao
from core.data_access import meter_reading_dao


class Journal:

    def __init__(self):
        self._mrs = journal_dao.find_all()

        for idx, val in enumerate(self._mrs):
            if idx > 0:
                val.consumption = val.value - prev_value
                val.days = (val.date - prev_date).days
            else:
                val.consumption = 0.0
                val.days = 0
            prev_value = val.value
            prev_date = val.date

    def __len__(self):
        return len(self._mrs)

    def __getitem__(self, i):
        return self._mrs[i]

    def __iter__(self):
        i = 0
        stop = len(self._mrs)
        while i < stop:
            yield self._mrs[i]
            i += 1

    @property
    def mean(self):
        try:
            mean = sum([mr.mean_consumption_per_day for mr in self._mrs[1:]]) / (len(self._mrs) - 1)
        except ZeroDivisionError:
            mean = 0
        finally:
            return float("{0:.2f}".format(mean))

    def trend_last_days(self, nbr_days):
        cpt_days = 0
        value = 0
        remaining_days = nbr_days

        for mr in self._mrs[::-1]:
            if mr.days > remaining_days:
                value += remaining_days * mr.mean_consumption_per_day
            else:
                value += mr.days * mr.mean_consumption_per_day

            cpt_days += mr.days
            remaining_days = nbr_days - cpt_days
            if remaining_days <= 0:
                break

        try:
            mean_last_days = value / nbr_days
            global_mean = sum([mr.mean_consumption_per_day for mr in self._mrs[1:]]) / (len(self._mrs) - 1)
            trend_last_days = float("{0:.2f}".format(mean_last_days / global_mean))
        except ZeroDivisionError:
            trend_last_days = 0
        finally:
            return "{0:.2f} %".format(-1 * (100 - (trend_last_days * 100)))

    def export_csv(self):
        path = "export.csv"
        with open(path, mode="w", encoding="UTF-8") as file:
            for mr in self._mrs:
                file.write("{},{}\n".format(mr.date, mr.value))
        return path

    def import_csv(self, file):
        line = file.readline().decode("utf-8")
        while line:
            line_list = line.split(',')
            value = line_list[1]
            date = line_list[0]
            meter_reading_dao.insert(core.models.MeterReading(date, value))
            line = file.readline().decode("utf-8")
