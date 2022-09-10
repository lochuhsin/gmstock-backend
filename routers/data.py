from fastapi import APIRouter, WebSocket

from internal.data_service import get_timeseries
from utils.util import unique_table_selector

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/stocks")
async def list_stock():
    return {"status": 204}


@router.get("/forexpair")
async def list_forexpair():
    return {"status": 204}


@router.get("/cryptocurrency")
async def list_cryptocurrency():
    return {"status": 204}


@router.get("/etf")
async def list_etf():
    return {"status": 204}


@router.get("/indices")
async def list_indices():
    return {"status": 204}


@router.get("/timeseries/{unique}")
async def list_timseries(unique: str):
    product, *_ = unique.split("_")
    unique_table = unique_table_selector(product)
    if unique not in unique_table:
        return {"status": 404, "message": "unique not found"}
    return {"status": 200, "result": get_timeseries(unique)}


@router.get("/uniques/{product_type}")
async def list_uniques(product_type: str):
    unique_table = unique_table_selector(product_type)
    return {"status": 200, "results": list(unique_table.get_uniques())}


@router.websocket("/timeseries")
async def timeseries_websocket(websocket: WebSocket):
    import time
    await websocket.accept()
    while True:
        time.sleep(1)
        await websocket.send_text(f"this is what u have sended: {'asdfasd'}")

