import logging
import time
from fastapi import FastAPI
from pymongo import MongoClient
from sqlalchemy_utils.functions import database_exists
from config import settings
from db.mongo import get_collections
from routers import data_controller, script_controller, testing
from utils.util import unique_table_selector
from utils.singleton import ScriptInfoCache
from db.info import get_scripts

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
app = FastAPI()
app.include_router(script_controller.router)
app.include_router(data_controller.router)
app.include_router(testing.router)

WAITTING_TIME = 10
RETRY = 5


@app.on_event("startup")
def check_mongodb_exist():
    client = MongoClient(settings.mongo_conn)
    db_list: list[str] = client.list_database_names()

    if settings.mongo_db_name not in db_list:
        raise ValueError(f"Database of {settings.mongo_db_name} not found !!!!!!")
    logger.info("mongo connection checking complete")


def __retry_db_conn(conn: str) -> bool:
    retry_count = 0
    while retry_count < RETRY:
        if database_exists(conn):
            return True
        time.sleep(WAITTING_TIME)
        retry_count += 1
    return False


@app.on_event("startup")
def check_postgres_exist():
    if not __retry_db_conn(settings.rmdb_postgres_conn):
        raise ValueError("Scheduler database doesn't exists")
    logger.info("Scheduler database checking complete")


# collection name rule
# stock_<symbol>_<mic_code>
# forexpair_<symbol>_<currency_base>
# cryptocurrency_<symbol>_<currency_base>
# etf_<symbol>_<mic_code>
# indices_<symbol>_<country>
@app.on_event("startup")
def initialize_symbol_table():
    logger.info("start initializing unique symbol singleton")

    for collection in get_collections():
        table, *_ = collection.split("_")
        if table == "dummy":
            continue
        unique_table = unique_table_selector(table)
        unique_table.add(collection)


@app.on_event("startup")
def initialize_script_cache():
    scripts = get_scripts()
    cache = ScriptInfoCache(((sc.name, sc.filepath) for sc in scripts))
    logger.info(len(cache))


@app.get("/")
async def root():
    return {"message": "Hello World"}
