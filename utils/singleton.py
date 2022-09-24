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

"""
There are two hashmap:
 1. id_unique, key: id, value: list of unique,
 2. unique_id_instance, key: unique, value: list of {id: instance}
 3. self.all_id_instance, key: id, value: instance
 Special Keyword: unique: "__all__"
"""


class ScriptInstanceCache(metaclass=Singleton):
    def __init__(self, id_script_instance: Iterable = None):
        self.id_unique: dict = defaultdict(list)
        self.unique_id_instance: dict = defaultdict(dict)
        self.all_id_instance: dict = {}
        if id_script_instance is not None:
            for _id, instance in id_script_instance:
                if not (uniques := instance.unique):
                    logger.info(f"script unique not defined, script id:{_id}")
                    continue

                if uniques == "__all__":
                    self.all_id_instance[_id] = instance
                    continue

                uniques: list = ScriptInstanceCache._convert_to_list(uniques)

                self.id_unique[_id] = uniques

                for unique in self.id_unique[_id]:
                    self.unique_id_instance[unique][_id] = instance

    def add_script_by_id(self, _id: int, script_instance) -> tuple[bool, str]:
        if _id in self.id_unique:
            return False, "instance may already exists"

        if not (uniques := script_instance.unique):
            return False, f"unique not defined, script id: {_id}"

        if uniques == "__all__":
            self.all_id_instance[_id] = script_instance
            return True, ""

        uniques: list = ScriptInstanceCache._convert_to_list(uniques)

        for unique in uniques:
            self.unique_id_instance[unique][_id] = script_instance
        self.id_unique[_id] = uniques

        return True, ""

    def get_script_by_unique(self, unique: str) -> tuple[bool, dict]:
        return True, self.unique_id_instance.get(unique, {})

    def get_script_all_unique(self) -> tuple[bool, dict]:
        return True, self.all_id_instance

    def upsert_script_by_id(self, _id: int, script_instance) -> tuple[bool, str]:
        try:
            if _id in self.id_unique or _id in self.all_id_instance:
                status, msg = self.update_script_by_id(_id, script_instance)
            else:
                status, msg = self.add_script_by_id(_id, script_instance)

            if not status:
                return status, msg

            return True, ""

        except Exception as e:
            return False, str(e)

    def update_script_by_id(self, _id: int, script_instance) -> tuple[bool, str]:
        try:
            if not (uniques := script_instance.unique):
                return False, "new script unique not defined"

            # remove all possible occurrences
            if _id in self.all_id_instance:
                del self.all_id_instance[_id]

            original_uniques = self.id_unique.get(_id)
            if not original_uniques:
                return False, "instance doesn't exists"

            for o_unique in original_uniques:
                instance_dict = self.unique_id_instance.get(o_unique)
                if _id not in instance_dict:
                    return False, "instance doesn't exist"

                del instance_dict[_id]

            # Add new instance
            if uniques == "__all__":
                self.all_id_instance[_id] = script_instance
                return True, ""

            uniques: list = ScriptInstanceCache._convert_to_list(uniques)

            for unique in uniques:
                self.unique_id_instance[unique][_id] = script_instance
            self.id_unique[_id] = uniques

        except Exception as e:
            return False, str(e)

        return True, ""

    def remove_script_by_id(self, _id: int) -> tuple[bool, str]:

        if _id not in self.id_unique and _id not in self.id_unique:
            return True, "id not exists"

        if _id in self.all_id_instance:
            del self.all_id_instance[_id]

        if _id in self.id_unique:
            uniques: list[str] = self.id_unique.get(_id)

            for unique in uniques:
                instance_dict = self.unique_id_instance.get(unique)
                if _id not in instance_dict:
                    continue
                del instance_dict[_id]

            del self.id_unique[_id]

        return True, ""

    @staticmethod
    def _convert_to_list(unique) -> list[str]:
        return unique if isinstance(type(unique), list) else [unique]


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
