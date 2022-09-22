from typing import Generator

from utils.singleton import MongoDB


def get_collections():
    return MongoDB().db.list_collection_names()


def get_timeserise_by_unique(unique: str) -> Generator:
    collection = MongoDB().db[unique]
    # exclude _id field
    return collection.find({}, {"_id": False})


def get_timeseries_insert_stream() -> Generator:
    pipeline = [{"$match": {"operationType": "insert"}}]
    with MongoDB().db.watch(pipeline) as stream:
        for insert_change in stream:
            yield insert_change


def get_timeseries_insert_stream_unique(unique: str) -> Generator:
    pipeline = [{"$match": {"operationType": "insert"}}]
    with MongoDB().db.collection[unique].watch(pipeline) as stream:
        for insert_change in stream:
            yield insert_change
