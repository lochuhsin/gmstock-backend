import logging
import requests
from fastapi import APIRouter, WebSocket
from config import settings
from utils.singleton import MongoDB
from db.mongo import get_collections
import importlib
import asyncio
from internal import data_service
from utils.util import parse_stream_to_json

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


@router.websocket("/ws")
async def test_ws(websocket: WebSocket):
    await websocket.accept()
    gen = data_service.test()
    while True:
        data = next(gen)
        logger.info(f"this is data {data}")
        json_str = parse_stream_to_json(data, "____test____")
        await websocket.send_json({"result": json_str})
        await asyncio.sleep(0.1)
