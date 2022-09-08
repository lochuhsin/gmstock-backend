import logging
from datetime import datetime

from fastapi import APIRouter, UploadFile

from internal.file_service import add_script, get_scripts

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/scripts", tags=["scripts"])


@router.get("/")
async def list_script():
    scripts: list = [] if not get_scripts() else get_scripts()
    return {"status": 204, "results": scripts}


@router.get("/{script_id}")
async def get_script(script_id):
    return {"status": 204}


@router.post("/")
async def create_script(description: str | None, file: UploadFile):
    upload_time = datetime.utcnow()
    add_script(description, upload_time, file)
    return {"status": 204, "filename": file.filename}


@router.patch("/{script_id}")
async def update_script(script_id, file: UploadFile):
    return {"status": 204, "script_id": script_id, "filename": file.filename}
