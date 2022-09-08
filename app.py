import logging
import time

from fastapi import FastAPI
from pymongo import MongoClient
from sqlalchemy_utils.functions import database_exists

from config import settings
from db.mongo import get_collections
from routers import script_controller, testing
from utils.singleton import UniqueLookUpTable

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
app = FastAPI()
app.include_router(script_controller.router)
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
    if not __retry_db_conn(settings.rmdb_backend_conn):
        raise ValueError("Backend database doesn't exists")
    logger.info("Backend database checking complete")

    if not __retry_db_conn(settings.rmdb_scheduler_conn):
        raise ValueError("Scheduler database doesn't exists")
    logger.info("Scheduler database checking complete")


@app.on_event("startup")
def initialize_symbol_table():
    UniqueLookUpTable(unique=get_collections())


@app.get("/")
async def root():
    return {"message": "Hello World"}
