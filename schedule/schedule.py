import logging
from db.mongo import get_collections
from utils.util import unique_table_selector

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


def update_product_tables():
    logger.info("start initializing unique symbol singleton")

    for collection in get_collections():
        table, *_ = collection.split("_")
        if table == "dummy":
            continue
        unique_table = unique_table_selector(table)
        unique_table.add(collection)
