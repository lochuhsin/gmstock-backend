import logging
import requests
from fastapi import APIRouter
from config import settings
from utils.singleton import MongoDB
from db.mongo import get_collections

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/collections")
def get_collection_list():
    collections = []
    for collection in get_collections():
        collections.append(collection)

    return {"status": 200, "collections": collections}


@router.get("/stocks")
def get_stocks():
    return {"status": 204}


@router.get("/test")
def test():
    resp = requests.get(settings.scheduler_conn + "twelveDataInfo")
    return resp.json()


@router.get("/mongodata")
def mongodata():
    collection = MongoDB().db["stocks_39YA_XDUS"]
    for obj in collection.find({}):
        logger.info(obj)
    return {}
