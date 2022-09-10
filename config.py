from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_conn: str = "mongodb://root:root@mongo:27017"
    mongo_db_name: str = "TimeSeries"

    rmdb_postgres_conn: str = "postgresql://root:root@postgres/postgres"

    scheduler_conn: str = "http://scheduler:3000/"
    debug: bool = True
    file_storage: str = "/app/files/"


settings = Settings()
