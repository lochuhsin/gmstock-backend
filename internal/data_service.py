from typing import Generator

from db.mongo import get_timeserise_by_unique


# TODO: add DTO model
def get_timeseries(unique) -> list[dict]:
    # preventing duplicate data
    datetime_set: set = set()
    timeseries: list = []
    timeseries_gen: Generator = get_timeserise_by_unique(unique)
    for obj in timeseries_gen:
        datatime = obj.get("datetime")
        if datatime in datetime_set:
            continue
        timeseries.append(obj)
        datetime_set.add(datatime)

    return timeseries
