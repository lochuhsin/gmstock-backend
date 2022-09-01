from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_conn: str = "mongodb://root:root@mongo:27017"
    mongo_db_name: str = "TimeSeries"
    rmdb_conn: str = ""
    debug: bool = True


settings = Settings()
