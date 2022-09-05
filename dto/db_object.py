from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Script(Base):
    __tablename__ = 'script'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    filepath = Column(String)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))


class Stocks(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    currency = Column(String)
    exchange = Column(String)
    mic_code = Column(String)
    country = Column(String)
    type_ = Column("type", String)
    latest_date = Column(DateTime(timezone=True))
    oldest_date = Column(DateTime(timezone=True))
    ishistorydatafinished = Column(Boolean)
    table_update_date = Column(DateTime(timezone=True))
    global_ = Column("global", String)


class ForexPair(Base):
    __tablename__ = 'forexpair'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    currency_group = Column(String)
    currency_base = Column(String)
    currency_quote = Column(String)
    latest_date = Column(DateTime(timezone=True))
    oldest_date = Column(DateTime(timezone=True))
    ishistorydatafinished = Column(Boolean)
    table_update_date = Column(DateTime(timezone=True))


class CryptoCurrency(Base):
    __tablename__ = 'cryptocurrency'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    available_exchange = Column(String)
    currency_base = Column(String)
    currency_quote = Column(String)
    latest_date = Column(DateTime(timezone=True))
    oldest_date = Column(DateTime(timezone=True))
    ishistorydatafinished = Column(Boolean)
    table_update_date = Column(DateTime(timezone=True))


class ETF(Base):
    __tablename__ = 'etf'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    currency = Column(String)
    exchange = Column(String)
    mic_code = Column(String)
    country = Column(String)
    latest_date = Column(DateTime(timezone=True))
    oldest_date = Column(DateTime(timezone=True))
    ishistorydatafinished = Column(Boolean)
    table_update_date = Column(DateTime(timezone=True))
    global_ = Column("global", String)


class Indices(Base):
    __tablename__ = 'indices'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    country = Column(String)
    currency = Column(String)
    latest_date = Column(DateTime(timezone=True))
    oldest_date = Column(DateTime(timezone=True))
    ishistorydatafinished = Column(Boolean)
    table_update_date = Column(DateTime(timezone=True))
    global_ = Column("global", String)
    plan = Column(String)
