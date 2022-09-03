from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_conn: str = "mongodb://root:root@mongo:27017"
    mongo_db_name: str = "TimeSeries"
    rmdb_backend_conn: str = "postgresql://root:root@postgres/backend"
    rmdb_scheduler_conn: str = "postgresql://root:root@postgres/postgres"
    scheduler_conn: str = "http://scheduler/"
    debug: bool = True


settings = Settings()
