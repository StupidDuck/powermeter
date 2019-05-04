from datetime import datetime
from core.data_access import journal_dao


class Journal:

    def __init__(self):
        self._mrs = journal_dao.find_all()

        for idx, val in enumerate(self._mrs):
            if idx > 0:
                val.consumption = val.value - prev_value
                val.days = (datetime.strptime(val.date, '%Y-%m-%d').date() - prev_date).days
            else:
                val.consumption = 0.0
                val.days = 0
            prev_value = val.value
            prev_date = datetime.strptime(val.date, '%Y-%m-%d').date()

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
        if len(self._mrs) > 0:
            mean = sum([mr.mean_consumption_per_day for mr in self._mrs[1:]]) / (len(self._mrs) - 1)
        else:
            mean = 0
        return float("{0:.2f}".format(mean))

    def trend_last_days(self, nbr_days):
        if nbr_days == 0:
            return 0.0

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

        mean_last_days = value / nbr_days
        global_mean = sum([mr.mean_consumption_per_day for mr in self._mrs[1:]]) / (len(self._mrs) - 1)
        trend_last_days = float("{0:.2f}".format(mean_last_days / global_mean))

        return "{} %".format(-1 * (100 - (trend_last_days * 100)))

    def export_csv(self):
        path = "export.csv"
        with open(path, mode="w", encoding="UTF-8") as file:
            for mr in self._mrs:
                file.write("{},{}\n".format(mr.date, mr.value))
        return path
