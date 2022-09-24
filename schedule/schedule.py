import logging

from db.info import get_scripts
from db.mongo import get_collections
from utils.singleton import ScriptInstanceCache
from utils.util import load_script_instance, unique_table_selector

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
    cache = ScriptInstanceCache()

    for sc in scripts:
        instance = load_script_instance(sc.filepath)
        status, msg = cache.upsert_script_by_id(sc.id, instance)
        if not status:
            logger.warning(
                f"during upsert script instance cache, following error: {msg}"
            )

    logger.info("Script cache update complete")
