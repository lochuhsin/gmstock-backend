import logging
from collections import defaultdict
from typing import Generator, Iterable

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings
from utils._singleton import Singleton

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class ScriptInstanceCache(metaclass=Singleton):
    def __init__(self, id_script_instance: Iterable[int, any] = None):

        self.id_unique: dict = defaultdict(str)
        self.unique_id_instance: dict = defaultdict(dict)

        for _id, instance in id_script_instance:
            if not (unique := instance.unique):
                logger.info(f"script unique not defined, script id:{_id}")
                continue

            self.id_unique[_id] = unique
            self.unique_id_instance[unique][_id] = instance

    def add_script_by_id(self, _id: int, script_instance) -> tuple[bool, str]:
        if _id in self.id_unique:
            return False, "instance may already exists"

        if not (unique := script_instance.unique):
            return False, f"unique not defined, script id: {_id}"

        self.unique_id_instance[unique][_id] = script_instance
        self.id_unique[_id] = unique

        return True, ""

    def get_script_by_unique(self, unique: str) -> tuple[bool, list]:

        if not (instances_dict := self.unique_id_instance.get(unique)):
            return False, []
        return True, instances_dict.values()

    def update_script_by_id(self, id: int, script_instance) -> tuple[bool, str]:
        try:
            if not (unique := script_instance.unique):
                return False, "new script unique not defined"

            original_unique = self.id_unique.get(id)
            if not original_unique:
                return False, "instance doesn't exists"

            instance_dict = self.unique_id_instance.get(original_unique)
            if id not in instance_dict:
                return False, "instance doesn't exist"

            # remove old instance no matter what
            del instance_dict[id]

            # add new instance with new unique
            self.unique_id_instance[unique] = script_instance

            # update id with it's unique
            self.id_unique[id] = unique
        except Exception as e:
            return False, str(e)

        return True, ""

    def remove_script_by_id(self, id: int) -> tuple[bool, str]:

        if id not in self.id_unique:
            return True, "id not exists"

        unique = self.id_unique.get(id)

        instance_dict = self.unique_id_instance.get(unique)
        if not instance_dict:
            return True, "unique not exists"

        del instance_dict[id]
        del self.id_unique[id]

        return True, ""


# key: id, value: {module, unique_list}
class ScriptInfoCache(metaclass=Singleton):
    def __init__(self, file_idpaths: Iterable[tuple] = None):
        self.id_path = (
            dict() if not file_idpaths else {_id: path for _id, path in file_idpaths}
        )

    def add(self, _id: int, path: str) -> tuple[bool, str]:
        if _id in self.id_path:
            return False, "file exists"
        self.id_path[_id] = path
        return True, ""

    def bulk_upsert(self, id_path: list[tuple[int, str]]) -> tuple[bool, str]:
        try:
            for _id, path in id_path:
                self.id_path[_id] = path
        except Exception as e:
            return False, str(e)
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
