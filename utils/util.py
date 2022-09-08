from enum import Enum

from utils.singleton import (
    UniqueCryptoCurrencyTable,
    UniqueETFTable,
    UniqueForexPairTable,
    UniqueIndicesTable,
    UniqueStocksTable,
)


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
