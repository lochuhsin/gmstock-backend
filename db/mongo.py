from typing import Generator

from utils.singleton import MongoDB


def get_collections():
    return MongoDB().db.list_collection_names()


def get_timeserise_by_unique(unique: str) -> Generator:
    collection = MongoDB().db[unique]
    # exclude _id field
    return collection.find({}, {"_id": False})
