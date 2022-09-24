import importlib
import json
import logging
from enum import Enum

from utils.singleton import (
    UniqueCryptoCurrencyTable,
    UniqueETFTable,
    UniqueForexPairTable,
    UniqueIndicesTable,
    UniqueStocksTable,
)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


def parse_stream_to_json(data: dict, unique) -> str:
    trade_info: dict = data.get("fullDocument")
    trade_info.pop("_id")
    trade_info["datetime"] = trade_info["datetime"].strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({"unique": unique, "trade_info": trade_info})


def load_script_instance(path: str) -> any:
    # remove extern
    pure_path = path[:-3]  # remove .py

    path_list = pure_path.split("/")
    del path_list[:2]
    module_path = ".".join(path_list)

    module = importlib.import_module(module_path)
    instance = module.CustomScript()
    return instance


class ProductType(Enum):
    Stock = "stocks"
    ForexPair = "forexpair"
    CryptoCurrency = "cryptocurrency"
    ETF = "etf"
    Indices = "indices"


def unique_table_selector(product_type: Enum | str):
    if product_type == ProductType.Stock or product_type == ProductType.Stock.value:
        return UniqueStocksTable()

    elif product_type == ProductType.ETF or product_type == ProductType.ETF.value:
        return UniqueETFTable()

    elif (
        product_type == ProductType.Indices or product_type == ProductType.Indices.value
    ):
        return UniqueIndicesTable()

    elif (
        product_type == ProductType.CryptoCurrency
        or product_type == ProductType.CryptoCurrency.value
    ):
        return UniqueCryptoCurrencyTable()

    elif (
        product_type == ProductType.ForexPair
        or product_type == ProductType.ForexPair.value
    ):
        return UniqueForexPairTable()

    else:
        return None
