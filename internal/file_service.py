import shutil
from datetime import datetime
import os
from config import settings
from db import info
from dto.db_object import Script


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

    info.insert_script(Script(
        name=filename,
        description=description,
        filepath=filepath,
        created_at=create_at,
        updated_at=create_at,
    ))


def rm_script(_id: int) -> None:
    # retrieve script information
    script: Script = get_script_by_id(_id)

    # remove file in local
    os.remove(script.filepath)

    # remove file information in database
    info.remove_script_by_id(_id)
