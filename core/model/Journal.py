from datetime import date, timedelta

class Journal:

    def __init__(self, indexes):
        self._indexes = indexes

        prev_value = 0
        prev_date = None
        for idx, val in enumerate(self._indexes):
            if idx > 0:
                val.consumption = val.value - prev_value
                val.days = (val.date - prev_date).days
                val.prev_date = prev_date
                val.prev_value = prev_value
            else:
                val.consumption = 0.0
                val.days = 0
                val.prev_date = None
                val.prev_value = 0
            prev_value = val.value
            prev_date = val.date

    def __len__(self):
        return len(self._indexes)

    def __getitem__(self, i):
        return self._indexes[i]

    def __iter__(self):
        i = 0
        stop = len(self._indexes)
        while i < stop:
            yield self._indexes[i]
            i += 1

    @property
    def mean(self, period_in_days=365):
        try:
            indexes = [mr for mr in self._indexes[1:] if mr.date >= (date.today() - timedelta(days=period_in_days))]
            mean = sum([mr.consumption for mr in indexes]) / sum([mr.days for mr in indexes])
            return float("{0:.2f}".format(mean))
        except ZeroDivisionError:
            return float("0.00")

    def trend_last_days(self, nbr_days):
        value_last_days = 0
        days_last_days = 0
        value_global = 0
        days_global = 0
        remaining_value = 0
        remaining_days = nbr_days

        if len(self._indexes) < 3:
            return "+ 0.00 %"

        for mr in self._indexes[:0:-1]:
            if remaining_days > 0:
                if mr.days > remaining_days:
                    value_last_days += remaining_days * mr.mean_consumption_per_day
                else:
                    value_last_days += mr.days * mr.mean_consumption_per_day
                days_last_days += mr.days
                remaining_days = nbr_days - days_last_days
                remaining_value = -1 * remaining_days * mr.mean_consumption_per_day
            else:
                if remaining_value > 0:
                    value_global += remaining_value
                    days_global += -1 * remaining_days
                    remaining_value = 0
                value_global += mr.days * mr.mean_consumption_per_day
                days_global += mr.days

        if days_last_days < nbr_days:
            return "+ 0.00 %"

        try:
            mean_last_days = value_last_days / nbr_days
            mean_global = value_global / days_global
            trend_last_days = mean_last_days / mean_global
            if trend_last_days < 1:
                return "- {0:.2f} %".format(((trend_last_days * 100) - 100) * -1)
            else:
                return "+ {0:.2f} %".format((trend_last_days * 100) -100)
        except ZeroDivisionError:
            return "+ 0.00 %"
