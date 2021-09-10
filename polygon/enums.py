# ========================================================= #
import enum
# ========================================================= #


# Ticker Market Types - Reference APIs
class TickerMarketType(enum.Enum):
    """
    Market Type to be used for method: ReferenceClient.get_tickers()
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Ticker Types - Reference APIs
class TickerType(enum.Enum):
    """
    Ticker type to be used for method: ReferenceClient.get_tickers()
    """
    CS = 'CS'
    COMMON_STOCKS = 'CS'
    ADRC = 'ADRC'
    ADRP = 'ADRP'
    ADRR = 'ADRR'
    UNIT = 'UNIT'
    RIGHT = 'RIGHT'
    PFD = 'PFD'
    FUND = 'FUND'
    SP = 'SP'
    WARRANT = 'WARRANT'
    INDEX = 'INDEX'
    ETF = 'ETF'
    ETN = 'ETN'


# Ticker Sort Type - Reference APIs
class TickerSortType(enum.Enum):
    """Sort key to be used for method: ReferenceClient.get_tickers()"""
    TICKER = 'ticker'
    NAME = 'name'
    MARKET = 'market'
    LOCALE = 'locale'
    PRIMARY_EXCHANGE = 'primary_exchange'
    TYPE = 'type'
    ACTIVE = 'active'
    CURRENCY_SYMBOL = 'currency_symbol'
    CURRENCY_NAME = 'currency_name'
    BASE_CURRENCY_SYMBOL = 'base_currency_symbol'
    BASE_CURRENCY_NAME = 'base_currency_name'
    CIK = 'cik'
    COMPOSITE_FIGI = 'composite_figi'
    SHARE_CLASS_FIGI = 'share_class_figi'
    LAST_UPDATED_UTC = 'last_updated_utc'
    DELISTED_UTC = 'delisted_utc'


# SORT Order - Common for most endpoints
class SortOrder(enum.Enum):
    """
    Order of sort. Ascending usually means oldest at the top. Descending usually means newest at the top. It is
    recommended to ensure the behavior in the corresponding function's docs. This enum can be used by any method
    accepting Sort order values.
    """
    ASCENDING = 'asc'
    ASC = 'asc'
    DESCENDING = 'desc'
    DESC = 'desc'


# Ticker Type Asset Class - Reference APIs
class TickerTypeAssetClass(enum.Enum):
    """
    Asset Class to be used for method: ReferenceClient.get_ticker_types_v3()
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Ticker Type Locales - Reference APIs
class TickerTypeLocale(enum.Enum):
    """
    Locale Type to be used for method: ReferenceClient.get_ticker_types_v3()
    """
    US = 'us'
    GLOBAL = 'global'


# Ticker News Sort - Reference APIs
class TickerNewsSort(enum.Enum):
    """
    Sort key to be used for method: ReferenceClient.get_ticker_news()
    """
    PUBLISHED_UTC = 'published_utc'
    ALL = None

# TODO: finish docstrings. Add enums.

# Stock Report Type - Reference APIs
class StockReportType(enum.Enum):
    YEAR = 'Y'
    Y = 'Y'
    YA = 'YA'
    YEAR_ANNUALIZED = 'YA'
    Q = 'Q'
    QUARTER = 'Q'
    QA = 'QA'
    QUARTER_ANNUALIZED = 'QA'
    T = 'T'
    TRAILING_TWELVE_MONTHS = 'T'
    TA = 'TA'
    TRAILING_TWELVE_MONTHS_ANNUALIZED = 'TA'


# Conditions Mapping Tick Type - Reference APIs
class ConditionMappingTickType(enum.Enum):
    TRADES = 'trades'
    QUOTES = 'quotes'


# Exchanges Asset Class
class ExchangesAssetClass(enum.Enum):
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Exchanges Locales - Reference APIs
class ExchangesLocale(enum.Enum):
    US = 'us'
    GLOBAL = 'global'


# Snapshot Direction - Stocks, Fx, Crypto APIs
class SnapshotDirection:
    """Direction to be supplied to the SnapShot - Gainers and Losers APIs on Stocks, Forex and Crypto endpoints"""
    GAINERS = 'gainers'
    GAIN = 'gainers'
    LOSERS = 'losers'
    LOSE = 'losers'


#

# ========================================================= #

if __name__ == '__main__':
    pass

# ========================================================= #
