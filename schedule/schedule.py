import logging

from db.info import get_scripts
from db.mongo import get_collections
from utils.singleton import ScriptInfoCache
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

    logger.info("unique collection update complete")


def update_script_cache():
    logger.info("start updating script cache")
    scripts = get_scripts()
    cache = ScriptInfoCache()
    status, msg = cache.bulk_upsert(
        id_path=list((sc.id, sc.filepath) for sc in scripts)
    )
    if not status:
        logger.error("Script cache update failed")
    logger.error("Script cache update complete")
