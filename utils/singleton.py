from typing import Generator, Iterable

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings
from utils._singleton import Singleton


class UniqueLookUpTable(metaclass=Singleton):
    def __init__(self, unique: Iterable[str] = None):
        self._unique_set: set = set(unique) if unique else set()

    def __len__(self):
        return len(self._unique_set)

    def __contains__(self, unique: str):
        return unique in self._unique_set

    def get_unique(self) -> Generator:
        for unique in self._unique_set:
            yield unique

    def update(self, unique: Iterable[str]):
        self._unique_set.update(unique)

    def clear(self):
        self._unique_set = {}

    def remove(self, symbol: str):
        if symbol in self._unique_set:
            self._unique_set.remove(symbol)


class BackendDB(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(settings.rmdb_backend_conn)
        self.session = Session(self.engine)


class SchedulerDB(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(settings.rmdb_scheduler_conn)
        self.session = Session(self.engine)


class MongoDB(metaclass=Singleton):
    def __init__(self):
        self.db = MongoClient(settings.mongo_conn)[settings.mongo_db_name]
