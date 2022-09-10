from typing import Generator, Iterable
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import settings
from utils._singleton import Singleton


class ScriptInfoCache(metaclass=Singleton):
    def __init__(self, file_namepaths: Iterable[tuple] = None):
        self.name_path = dict() if not file_namepaths else {name: path for name, path in file_namepaths}

    def add(self, name, path) -> tuple[bool, str]:
        if name in self.name_path:
            return False, "file exists"
        self.name_path[name] = path
        return True, ""

    def update(self, name: str, path: str) -> tuple[bool, str]:
        if name not in self.name_path:
            return False, "file not exists"
        self.name_path[name] = path
        return True, ""

    def clear(self) -> tuple[bool, str]:
        self.name_path = dict()
        return True, ""

    def remove(self, name: str) -> tuple[bool, str]:
        if name not in self.name_path:
            return False, "file not exists"
        del self.name_path[name]
        return True, ""

    def get_path_by_name(self, name: str) -> tuple[bool, str]:
        if name not in self.name_path:
            return False, "file not exists"
        return True, self.name_path[name]

    def get_name_list(self) -> tuple[bool, list]:
        return True, list(self.name_path.keys())

    def __contains__(self, name: str):
        return name in self.name_path

    def __len__(self):
        return len(self.name_path)


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
