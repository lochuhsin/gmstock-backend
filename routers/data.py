import asyncio
import logging

from fastapi import APIRouter, HTTPException, WebSocket

from internal.data_service import (
    get_timeseries,
    timeseries_stream,
    timeseries_stream_unique,
)
from utils.util import ProductType, parse_stream_to_json, unique_table_selector

router = APIRouter(prefix="/data", tags=["data"])
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


@router.get("/product_type")
async def list_products():
    return {"status": 200, "product_type": [p.value for p in ProductType]}


@router.get("/timeseries/{unique}")
async def list_timeseries(unique: str):
    product, *_ = unique.split("_")
    unique_table = unique_table_selector(product)
    if unique not in unique_table:
        return {"status": 404, "message": "unique not found"}
    return {"status": 200, "result": get_timeseries(unique)}


@router.get("/uniques/{product_type}")
async def list_uniques(product_type: str):
    unique_table = unique_table_selector(product_type)
    if unique_table is None:
        raise HTTPException(400, "Product type not supported")
    return {"status": 200, "results": list(unique_table.get_uniques())}


@router.websocket("/timeseries/original/ws")
async def timeseries_origin(websocket: WebSocket):
    await websocket.accept()
    stream = timeseries_stream()
    while True:
        data = next(stream)
        await asyncio.sleep(0.01)
        unique: str = data.get("ns").get("coll")
        json_str: str = parse_stream_to_json(data, unique)
        await websocket.send_json(json_str)


@router.websocket("/timeseries/{unique}/ws")
async def timeseries_origin_unique(unique: str, websocket: WebSocket):

    # implement get last 1000 days data
    await websocket.accept()
    stream = timeseries_stream_unique(unique)
    while True:
        for data in stream:
            json_str = parse_stream_to_json(data, unique)
            await websocket.send_text(json_str)


@router.websocket("/timeseries/calculated/ws")
async def timeseries_calculated(websocket: WebSocket):
    await websocket.accept()
    while True:
        break
