from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings


def scheduler_db() -> Session:
    engine = create_engine(settings.rmdb_scheduler_conn)
    return Session(engine)


def backend_db() -> Session:
    engine = create_engine(settings.rmdb_backend_conn)
    return Session(engine)
