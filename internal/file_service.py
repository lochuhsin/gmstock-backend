import os
import shutil
from datetime import datetime

from fastapi import HTTPException

from config import settings
from db import info
from dto.db_object import Script
from utils.singleton import ScriptInfoCache


def get_scripts() -> list | None:
    return [script for script in info.get_scripts()]


def get_script_by_id(_id: int) -> Script:
    return info.get_script_by_id(_id)


def _savefile(filename: str, file) -> str:
    filepath = settings.file_storage + filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return filepath


def add_script(description: str | None, create_at: datetime, file) -> None:
    filename: str = file.filename
    filepath: str = _savefile(file.filename, file)

    script_id = info.insert_script(
        Script(
            name=filename,
            description=description,
            filepath=filepath,
            created_at=create_at,
            updated_at=create_at,
        )
    )

    cache = ScriptInfoCache()
    status, msg = cache.add(script_id, filepath)

    if not status:
        raise HTTPException(400, f"cache update message: {msg}")


def rm_script(_id: int) -> None:
    # retrieve script information
    script: Script = get_script_by_id(_id)

    # remove script in cache
    cache = ScriptInfoCache()
    status, msg = cache.remove(_id)
    if not status:
        raise HTTPException(400, f"cache remove message: {msg}")

    # remove file in local
    os.remove(script.filepath)

    # remove file information in database
    info.remove_script_by_id(_id)
