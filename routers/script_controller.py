from fastapi import APIRouter, UploadFile
from internal.info_service import get_scripts, add_script
import datetime
import logging
import os
router = APIRouter(prefix="/scripts",
                   tags=["scripts"])


@router.get("/")
async def list_script():
    scripts: list = [] if not get_scripts() else get_scripts()
    return {"status": 204, "results": scripts}


@router.get("/{script_id}")
async def get_script(script_id):
    return {"status": 204}


@router.post("/")
async def create_script(file: UploadFile):
    upload_time = datetime.datetime.utcnow()
    # filepath: str = add_script(upload_time, file.filename, file.file)

    import shutil
    from config import settings
    from io import BytesIO
    with open(settings.file_storage + file.filename, 'wb') as f:
        # shutil.copy2(file.file.name, settings.file_storage + file.filename)
        shutil.copyfileobj(file.file, f)
    logging.error(type(file.file))
    return {"status": 204, "filename": file.filename}


@router.patch("/{script_id}")
async def update_script(script_id, file: UploadFile):
    return {"status": 204, "script_id": script_id, "filename": file.filename}
