import logging

import requests
from fastapi import APIRouter
from config import settings
from utils.singleton import MongoDB

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/test", tags=["test"])


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
