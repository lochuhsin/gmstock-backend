from fastapi import APIRouter, WebSocket, HTTPException
from internal.data_service import get_timeseries, timeseries_stream
from utils.util import unique_table_selector, ProductType
import json

router = APIRouter(prefix="/data", tags=["data"])


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


@router.websocket("/timeseries/ws")
async def timeseries_origin(websocket: WebSocket):
    await websocket.accept()
    while True:
        stream = timeseries_stream()
        for data in stream:
            unique: str = data.get("ns").get("coll")
            trade_info: dict = data.get("fullDocument")
            trade_info.pop("_id")
            trade_info["datetime"] = trade_info["datetime"].strftime("%Y-%m-%d %H:%M:%S")
            json_str = json.dumps(
                {
                    "unique": unique,
                    "trade_info": trade_info
                }
            )
            await websocket.send_text(json_str)

