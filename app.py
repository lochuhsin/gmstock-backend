from fastapi import FastAPI
import pymongo
import logging
from config import settings
from routers import script_management

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
app = FastAPI()
app.include_router(script_management.router)


@app.on_event("startup")
def check_mongodb_exist():
    client = pymongo.MongoClient(settings.mongo_conn)
    db_list: list[str] = client.list_database_names()

    if settings.mongo_db_name not in db_list:
        raise ValueError(f"Database of {settings.mongo_db_name} not found !!!!!!")
    logger.info("mongo connection checking complete")


@app.get("/")
async def root():
    return {"message": "Hello World"}



