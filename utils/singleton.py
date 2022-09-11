from typing import Generator, Iterable
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import settings
from utils._singleton import Singleton


class ScriptInfoCache(metaclass=Singleton):
    def __init__(self, file_idpaths: Iterable[tuple] = None):
        self.id_path = dict() if not file_idpaths else {_id: path for _id, path in file_idpaths}

    def add(self, _id: int, path: str) -> tuple[bool, str]:
        if _id in self.id_path:
            return False, "file exists"
        self.id_path[_id] = path
        return True, ""

    def update(self, _id: int, path: str) -> tuple[bool, str]:
        if _id not in self.id_path:
            return False, "file not exists"
        self.id_path[_id] = path
        return True, ""

    def clear(self) -> tuple[bool, str]:
        self.id_path = dict()
        return True, ""

    def remove(self, _id: int) -> tuple[bool, str]:
        if _id not in self.id_path:
            return False, "file not exists"
        del self.id_path[_id]
        return True, ""

    def get_path_by_id(self, _id: int) -> tuple[bool, str]:
        if _id not in self.id_path:
            return False, "file not exists"
        return True, self.id_path[_id]

    def get_id_list(self) -> tuple[bool, list]:
        return True, list(self.id_path.keys())

    def __contains__(self, _id: int):
        return _id in self.id_path

    def __len__(self):
        return len(self.id_path)


class ErrorScriptInfoCache(metaclass=Singleton):
    def __init__(self):
        ...


class UniqueLookUpTableBase(metaclass=Singleton):
    def __init__(self, unique: Iterable[str] = None):
        self._unique_set: set = set(unique) if unique else set()

    def __len__(self):
        return len(self._unique_set)

    def __contains__(self, unique: str):
        return unique in self._unique_set

    def get_uniques(self) -> Generator:
        for unique in self._unique_set:
            yield unique

    def add(self, unique: str) -> tuple[bool, str]:
        self._unique_set.add(unique)
        return True, ""

    def update(self, unique: Iterable[str]) -> tuple[bool, str]:
        try:
            self._unique_set.update(unique)

        except Exception:
            return False, str(Exception)
        return True, ""

    def clear(self) -> tuple[bool, str]:
        self._unique_set = {}
        return True, ""

    def remove(self, unique: str) -> tuple[bool, str]:
        if unique in self._unique_set:
            self._unique_set.remove(unique)

            return True, ""
        return False, "unique not in look up table"


class UniqueStocksTable(UniqueLookUpTableBase):
    ...


class UniqueIndicesTable(UniqueLookUpTableBase):
    ...


class UniqueETFTable(UniqueLookUpTableBase):
    ...


class UniqueCryptoCurrencyTable(UniqueLookUpTableBase):
    ...


class UniqueForexPairTable(UniqueLookUpTableBase):
    ...


class PostgresDB(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(settings.rmdb_postgres_conn)
        self.session = Session(self.engine)


class MongoDB(metaclass=Singleton):
    def __init__(self):
        self.db = MongoClient(settings.mongo_conn)[settings.mongo_db_name]
