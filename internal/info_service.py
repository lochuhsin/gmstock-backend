from db import info_db
from datetime import datetime
from config import settings
import shutil


def get_scripts() -> list | None:
    return [script for script in info_db.get_scripts()]


def _savefile(filename: str, file) -> str:
    filepath = f"{settings.file_storage}{filename}"
    with open(filepath, 'w') as f:
        shutil.copyfileobj(file, f)
    return filepath


def add_script(time: datetime, filename: str, file: object) -> str:
    filepath: str = _savefile(filename, file)
    return filepath
