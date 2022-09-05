from fastapi import APIRouter

router = APIRouter(prefix="/data",
                   tags=["scripts"])


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