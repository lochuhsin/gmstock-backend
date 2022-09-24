import copy
import logging
from typing import Generator

from db.mongo import (
    get_timeseries_insert_stream,
    get_timeseries_insert_stream_unique,
    get_timeserise_by_unique,
)
from utils.singleton import ScriptInstanceCache

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


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


def timeseries_stream() -> Generator:
    stream: Generator = get_timeseries_insert_stream()
    return stream


def timeseries_stream_unique(unique: str) -> Generator:
    stream: Generator = get_timeseries_insert_stream_unique(unique)
    return stream


def loop_script_dict(data, script_dict: dict) -> Generator:
    for _id, instance in script_dict.items():
        new_data = copy.deepcopy(data)

        full_document = new_data.get("fullDocument")
        doc_id = full_document.pop("_id")
        doc_datetime = full_document.pop("datetime")

        status, updated_doc = instance.run_script(new_data.get("fullDocument"))
        # must implement error handling

        updated_doc["_id"] = doc_id
        updated_doc["datetime"] = doc_datetime
        new_data["fullDocument"] = updated_doc

        yield new_data


def timeseries_stream_calculated() -> Generator:
    cache = ScriptInstanceCache()
    stream: Generator = get_timeseries_insert_stream()
    for data in stream:
        unique: str = data.get("ns").get("coll")
        status, script_dict = cache.get_script_by_unique(unique)
        status, script_dict_all = cache.get_script_all_unique()

        for res in loop_script_dict(data, script_dict):
            yield res

        for res in loop_script_dict(data, script_dict_all):
            yield res
