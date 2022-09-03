from fastapi import APIRouter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config import settings
from dto.db_resp import Stocks
import requests

router = APIRouter(prefix="/test",
                   tags=["test"])


@router.get("/stocks")
def get_stocks():
    engine = create_engine(settings.rmdb_scheduler_conn)
    session = Session(engine)
    query = select(Stocks)
    resp = session.scalars(query)

    count = 0
    for _ in resp:
        count += 1

    return {"status": 204, "resp": count}


@router.get("/test")
def test():
    return requests.get(settings.scheduler_conn + "twelveDataInfo")
