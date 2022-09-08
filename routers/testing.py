import logging

import requests
from fastapi import APIRouter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from config import settings
from dto.db_object import Stocks
from utils.singleton import MongoDB

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/stocks")
def get_stocks():
    engine = create_engine(settings.rmdb_scheduler_conn)
    session = Session(engine)
    query = select(Stocks)
    resp = session.scalars(query)  # generator
    logging.error(type(resp))
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
