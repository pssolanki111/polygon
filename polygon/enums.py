# ========================================================= #
import enum
# ========================================================= #


# Ticker Market Types - Reference APIs
class TickerMarketType(enum.Enum):
    """
    Market Types for method: ``ReferenceClient.get_tickers()``
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Ticker Types - Reference APIs
class TickerType(enum.Enum):
    """
    Ticker types for method: ``ReferenceClient.get_tickers()``
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
    """Sort key for method: ``ReferenceClient.get_tickers()``"""
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
    Asset Class for method: ``ReferenceClient.get_ticker_types_v3()``
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Ticker News Sort - Reference APIs
class TickerNewsSort(enum.Enum):
    """
    Sort key for method: ``ReferenceClient.get_ticker_news()``
    """
    PUBLISHED_UTC = 'published_utc'
    ALL = None


# Stock Report Type - Reference APIs
class StockReportType(enum.Enum):
    """
    Type of report for method: ``ReferenceClient.get_stock_financials()``
    """
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


# Stock Report Sort Type - Reference APIs
class StockFinancialsSortType(enum.Enum):
    """
    Direction to use for sorting report for method: ``ReferenceClient.get_stock_financials()``
    """
    REPORT_PERIOD = 'reportPeriod'
    REVERSE_REPORT_PERIOD = '-reportPeriod'
    CALENDAR_DATE = 'calendarDate'
    REVERSE_CALENDAR_DATE = '-calendarDate'


# Stock Financial Time Frame - Reference APIs
class StockFinancialsTimeframe(enum.Enum):
    """
    Query by timeframe. Annual financials originate from 10-K filings, and quarterly financials originate from 10-Q
    filings. Note: Most companies do not file quarterly reports for Q4 and instead include those financials in their
    annual report, so some companies my not return quarterly financials for Q4
    for method: ``ReferenceClient.get_stock_financials_vx()``
    """
    ANNUAL = 'annual'
    QUARTERLY = 'quarterly'


# Stock Financials Sort Key - Reference APIS
class StockFinancialsSortKey(enum.Enum):
    """
    Sort field for method: ``ReferenceClient.get_stock_financials_vx()``
    """
    FILLING_DATE = 'filling_date'
    PERIOD_OF_REPORT_DATE = 'period_of_report_date'


# Conditions Mapping Tick Type - Reference APIs
class ConditionMappingTickType(enum.Enum):
    """
    Tick Type for method: ``ReferenceClient.get_condition_mappings()``
    """
    TRADES = 'trades'
    QUOTES = 'quotes'


# Conditions Data Type - Reference APIs
class ConditionsDataType(enum.Enum):
    """
    Type of data for method: ``ReferenceClient.get_conditions()``
    """
    TRADE = 'trade'
    BBO = 'bbo'
    NBBO = 'nbbo'


# Conditions SIP - Reference APIs
class ConditionsSIP(enum.Enum):
    """
    SIP for method: ``ReferenceClient.get_conditions()``
    """
    CTA = 'CTA'
    UTP = 'UTP'
    OPRA = 'OPRA'


# Conditions Sort key - Reference APIs
class ConditionsSortKey(enum.Enum):
    """
    Sort key for method: ``ReferenceClient.get_conditions()``
    """
    ASSET_CLASS = 'asset_class'
    ID = 'id'
    TYPE = 'type'
    NAME = 'name'
    DATA_TYPES = 'data_types'
    LEGACY = 'legacy'


# Asset Class - Common
class AssetClass(enum.Enum):
    """
    Asset Class for methods: ``ReferenceClient.get_exchanges_v3()`` and ``ReferenceClient.get_conditions()`` and
    wherever needed.
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'fx'
    CRYPTO = 'crypto'


# Locales - common
class Locale(enum.Enum):
    """
    Locale name``
    """
    US = 'us'
    GLOBAL = 'global'


# Snapshot Direction - Stocks, Fx, Crypto APIs
class SnapshotDirection:
    """Direction to be supplied to the SnapShot - Gainers and Losers APIs on Stocks, Forex and Crypto endpoints"""
    GAINERS = 'gainers'
    GAIN = 'gainers'
    LOSERS = 'losers'
    LOSE = 'losers'


# Stream Cluster - Websockets
class StreamCluster(enum.Enum):
    """
    The cluster to connect to. To be used for both callback and async stream client. NEVER connect to the same
    cluster again if there is an existing stream connected to it. The existing connection would be dropped and new
    one will be established. You can have up to 4 concurrent streams connected to 4 different clusters.
    """
    STOCKS = 'stocks'
    OPTIONS = 'options'
    FOREX = 'forex'
    CRYPTO = 'crypto'


# Options Contract Type - Common
class OptionsContractType(enum.Enum):
    """
    Contract Type for method: ``ReferenceClient.get_options_contracts()``
    """
    CALL = 'call'
    PUT = 'put'
    OTHER = 'other'


# Option contract Sort Key - Options
class OptionsContractsSortType(enum.Enum):
    """
    Sort field used for ordering for method: ``ReferenceClient.get_options_contracts()``
    """
    TICKER = 'ticker'
    UNDERLYING_TICKER = 'underlying_ticker'
    EXPIRATION_DATE = 'expiration_date'
    STRIKE_PRICE = 'strike_price'


# Option Trades Sort Type - Options
class OptionTradesSort(enum.Enum):
    """
    Sort field used for ordering option trades. Used for method: ``OptionsClient.get_trades``
    """

    TIMESTAMP = 'timestamp'


# Stocks Trades Sort Type - Stocks
class StocksTradesSort(enum.Enum):
    """
    Sort field used for ordering Stocks trades. Used for method: ``StocksClient.get_trades``
    """

    TIMESTAMP = 'timestamp'


# Stocks Quotes Sort Type - Stocks
class StocksQuotesSort(enum.Enum):
    """
    Sort field used for ordering Stocks quotes. Used for method: ``StocksClient.get_quotes``
    """

    TIMESTAMP = 'timestamp'


# Stocks Splits Sort Type - References
class SplitsSortKey(enum.Enum):
    """
    Sort field used for ordering stock splits. Used for method ``ReferenceClient.get_stock_splits``
    """

    EXECUTION_DATE = 'execution_date'
    TICKER = 'ticker'


# Stocks Dividends Payout Frequency - References
class PayoutFrequency(enum.Enum):
    """
    the number of times per year the dividend is paid out. Possible values are 0 (one-time), 1 (annually),
    2 (bi-annually), 4 (quarterly), and 12 (monthly). used by method ``ReferenceClient.get_stock_dividends``
    """

    ONE_TIME = 0
    ANNUALLY = 1
    BI_ANNUALLY = 2
    QUARTERLY = 4
    MONTHLY = 12


# Stock dividend Type - References
class DividendType(enum.Enum):
    """
    the type of dividend. Dividends that have been paid and/or are expected to be paid on consistent schedules
    are denoted as CD. Special Cash dividends that have been paid that are infrequent or unusual, and/or can not be
    expected to occur in the future are denoted as SC. Used for method ``ReferenceClient.get_stock_dividends``
    """

    CD = 'CD'
    SC = 'SC'
    LT = 'LT'
    ST = 'ST'


# Stock Dividend Sort - References
class DividendSort(enum.Enum):
    """
    sort field used for ordering dividend results. used for method ``ReferenceClient.get_stock_dividends``
    """

    EX_DIVIDEND_DATE = 'ex_dividend_date'
    PAY_DATE = 'pay_date'
    DECLARATION_DATE = 'declaration_date'
    RECORD_DATE = 'record_date'
    CASH_AMOUNT = 'cash_amount'
    TICKER = 'ticker'


# Forex Quotes Sort Type - Forex
class ForexQuotesSort(enum.Enum):
    """
    Sort field used for ordering Forex quotes. Used for method: ``ForexClient.get_quotes``
    """

    TIMESTAMP = 'timestamp'


# Crypto Trades Sort Type - Crypto
class CryptoTradesSort(enum.Enum):
    """
    Sort field used for ordering crypto trades. Used for method: ``CryptoClient.get_trades``
    """

    TIMESTAMP = 'timestamp'


# Stream Host - Common Websockets
class StreamHost(enum.Enum):
    """
    Host to be used for stream connections. WHY on earth would you use delayed if you're paying for polygon??
    """
    REAL_TIME = 'socket.polygon.io'
    DELAYED = 'delayed.polygon.io'


# Stream Service Prefix - Websockets
class StreamServicePrefix(enum.Enum):
    """
    Service Prefix for Stream endpoints. To be used for method: ``AsyncStreamClient.async change_handler()``
    """
    STOCK_TRADES = 'T'
    STOCK_QUOTES = 'Q'
    STOCK_MINUTE_AGGREGATES = 'AM'
    STOCK_SECOND_AGGREGATES = 'A'
    STOCK_LULD = 'LULD'
    STOCK_IMBALANCES = 'NOI'
    FOREX_QUOTES = 'C'
    FOREX_MINUTE_AGGREGATES = 'CA'
    CRYPTO_TRADES = 'XT'
    CRYPTO_QUOTES = 'XQ'
    CRYPTO_LEVEL2 = 'XL2'
    CRYPTO_MINUTE_AGGREGATES = 'XA'
    STATUS = 'status'
    OPTION_TRADES = 'T'
    OPTION_MINUTE_AGGREGATES = 'AM'
    OPTION_SECOND_AGGREGATES = 'A'


# Timespan - common
class Timespan(enum.Enum):
    """
    The timespan values. Usually meant for aggregates endpoints. It is best to consult the relevant docs before using
    any value on an endpoint.
    """
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'


# ========================================================= #

if __name__ == '__main__':
    pass

# ========================================================= #
