# ========================================================= #
from .. import base_client
from typing import Union
import datetime
from requests.models import Response
from httpx import Response as HttpxResponse

# ========================================================= #


def CryptoClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST crypto endpoints.

    :param api_key: Your API Key. Visit your dashboard to get yours.
    :param use_async: Set it to ``True`` to get async client. Defaults to usual non-async client.
    :param connect_timeout: The connection timeout in seconds. Defaults to 10. basically the number of seconds to
                            wait for a connection to be established. Raises a ``ConnectTimeout`` if unable to
                            connect within specified time limit.
    :param read_timeout: The read timeout in seconds. Defaults to 10. basically the number of seconds to wait for
                         date to be received. Raises a ``ReadTimeout`` if unable to connect within the specified
                         time limit.
    """

    if not use_async:
        return SyncCryptoClient(api_key, connect_timeout, read_timeout)

    return AsyncCryptoClient(api_key, connect_timeout, read_timeout)


# ========================================================= #


class SyncCryptoClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the crypto REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import CryptoClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    def get_historic_trades(self, from_symbol: str, to_symbol: str, date, offset: Union[str, int] = None,
                            limit: int = 500, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get historic trade ticks for a cryptocurrency pair.
        `Official Docs
        <https://polygon.io/docs/get_v1_historic_crypto__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the crypto pair.
        :param to_symbol: The "to" symbol of the crypto pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm trying to  think of a good way to implement pagination in the library for these endpoints
                       which do not return a ``next_url`` attribute.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.datetime, datetime.date)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/historic/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_trades(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                   timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                   raw_response: bool = False) -> Union[Response, dict]:
        """
        Get trades for a crypto ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_trades__cryptoTicker__anchor>`__

        :param symbol: The ticker symbol you want trades for. eg ``X:BTC-USD``. you can pass withor without the
                       prefix ``C:``
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.CryptoTradesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/trades/{symbol}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_last_trade(self, from_symbol: str, to_symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the last trade tick for a cryptocurrency pair.
        `Official Docs
        <https://polygon.io/docs/get_v1_last_crypto__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last/crypto/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_daily_open_close(self, from_symbol: str, to_symbol: str, date, adjusted: bool = True,
                             raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the open, close prices of a cryptocurrency symbol on a certain day.
        `Official Docs: <https://polygon.io/docs/get_v1_open-close_crypto__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param date: The date of the requested open/close. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/open-close/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='day',
                           adjusted: bool = True, sort='asc', limit: int = 5000,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get aggregate bars for a cryptocurrency pair over a given date range in custom time window sizes.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without prefix
                       ``X:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, (datetime.datetime, datetime.date)):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, (datetime.datetime, datetime.date)):
            to_date = to_date.strftime('%Y-%m-%d')

        timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
                f'{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire cryptocurrency market.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_crypto__date__anchor>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.datetime, datetime.date)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/global/market/crypto/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified cryptocurrency pair.
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without the
                       prefix ``X:``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        cryptocurrency symbols
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers_anchor>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded cryptocurrency symbol.
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__anchor>`__

        :param symbol: Symbol of the currency pair. eg: ``X:BTCUSD``. you can specify with or without prefix ``X:``
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{ensure_prefix(symbol).upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction='gainers', raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current top 20 gainers or losers of the day in cryptocurrency markets.
        `Official docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto__direction__anchor>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/{self._change_enum(direction, str)}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_level2_book(self, symbol: str, raw_response: bool = False) -> Union[Response, dict]:
        """
        Get the current level 2 book of a single ticker. This is the combined book from all of the exchanges.
        `Official Docs
        <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__book_anchor>`__

        :param symbol: The cryptocurrency ticker. eg: ``X:BTCUSD``. You can specify with or without the prefix ```X:``
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{ensure_prefix(symbol).upper()}/book'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #

class AsyncCryptoClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the crypto REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import CryptoClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    async def get_historic_trades(self, from_symbol: str, to_symbol: str,
                                  date, offset: Union[str, int] = None, limit: int = 500,
                                  raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get historic trade ticks for a cryptocurrency pair - Async method.
        `Official Docs
        <https://polygon.io/docs/get_v1_historic_crypto__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the crypto pair.
        :param to_symbol: The "to" symbol of the crypto pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm trying to  think of a good way to implement pagination in the library for these endpoints
                       which do not return a ``next_url`` attribute.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.datetime, datetime.date)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v1/historic/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_trades(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                         timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                         raw_response: bool = False) -> Union[Response, dict]:
        """
        Get trades for a crypto ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/get_vX_trades__cryptoTicker__anchor>`__

        :param symbol: The ticker symbol you want trades for. eg ``X:BTC-USD``. you can pass withor without the
                       prefix ``C:``
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.CryptoTradesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string.
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string.
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string.
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(timestamp, (datetime.date, datetime.datetime)):
            timestamp = timestamp.strftime('%Y-%m-%d')

        if isinstance(timestamp_lt, (datetime.date, datetime.datetime)):
            timestamp_lt = timestamp_lt.strftime('%Y-%m-%d')

        if isinstance(timestamp_lte, (datetime.date, datetime.datetime)):
            timestamp_lte = timestamp_lte.strftime('%Y-%m-%d')

        if isinstance(timestamp_gt, (datetime.date, datetime.datetime)):
            timestamp_gt = timestamp_gt.strftime('%Y-%m-%d')

        if isinstance(timestamp_gte, (datetime.date, datetime.datetime)):
            timestamp_gte = timestamp_gte.strftime('%Y-%m-%d')

        _path = f'/vX/trades/{ensure_prefix(symbol)}'

        _data = {'timestamp': timestamp, 'timestamp_lt': timestamp_lt, 'timestamp_lte': timestamp_lte,
                 'timestamp_gt': timestamp_gt, 'timestamp_gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_last_trade(self, from_symbol: str, to_symbol: str,
                             raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the last trade tick for a cryptocurrency pair - Async method
        `Official Docs
        <https://polygon.io/docs/get_v1_last_crypto__from___to__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last/crypto/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_daily_open_close(self, from_symbol: str, to_symbol: str, date, adjusted: bool = True,
                                   raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the open, close prices of a cryptocurrency symbol on a certain day - Async method
        `Official Docs: <https://polygon.io/docs/get_v1_open-close_crypto__from___to___date__anchor>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param date: The date of the requested open/close. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/open-close/crypto/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1,
                                 timespan='day', adjusted: bool = True, sort='asc',
                                 limit: int = 5000, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        et aggregate bars for a cryptocurrency pair over a given date range in custom time window sizes.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘5’`` then 5-minute bars will be returned - Async method
        `Official Docs
        <https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__range__multiplier___timespan___from___to__anchor>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without prefix
                       ``X:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(from_date, (datetime.datetime, datetime.date)):
            from_date = from_date.strftime('%Y-%m-%d')

        if isinstance(to_date, (datetime.datetime, datetime.date)):
            to_date = to_date.strftime('%Y-%m-%d')

        timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/range/{multiplier}/{timespan}/{from_date}/' \
                f'{to_date}'

        _data = {'adjusted': 'true' if adjusted else 'false',
                 'sort': sort,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_grouped_daily_bars(self, date, adjusted: bool = True,
                                     raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire cryptocurrency market - Async method
        `Official Docs <https://polygon.io/docs/get_v2_aggs_grouped_locale_global_market_crypto__date__anchor>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if isinstance(date, (datetime.datetime, datetime.date)):
            date = date.strftime('%Y-%m-%d')

        _path = f'/v2/aggs/grouped/locale/global/market/crypto/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_previous_close(self, symbol: str, adjusted: bool = True,
                                 raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified cryptocurrency pair - Async method
        `Official Docs <https://polygon.io/docs/get_v2_aggs_ticker__cryptoTicker__prev_anchor>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without the
                       prefix ``X:``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{ensure_prefix(symbol).upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot_all(self, symbols: list, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        cryptocurrency symbols - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers_anchor>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded cryptocurrency symbol - Async method
        `Official Docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__anchor>`__

        :param symbol: Symbol of the currency pair. eg: ``X:BTCUSD``. you can specify with or without prefix ``X:``
        :param raw_response: Whether or not to return the Response Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{ensure_prefix(symbol).upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_gainers_and_losers(self, direction='gainers',
                                     raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current top 20 gainers or losers of the day in cryptocurrency markets - Async method
        `Official docs <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto__direction__anchor>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/{self._change_enum(direction, str)}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_level2_book(self, symbol: str, raw_response: bool = False) -> Union[HttpxResponse, dict]:
        """
        Get the current level 2 book of a single ticker. combined book from all of the exchanges - Async method
        `Official Docs
        <https://polygon.io/docs/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__book_anchor>`__

        :param symbol: The cryptocurrency ticker. eg: ``X:BTCUSD``. You can specify with or without the prefix ```X:``.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/crypto/tickers/{ensure_prefix(symbol).upper()}/book'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


def ensure_prefix(sym: str):
    if sym.upper().startswith('X:'):
        return sym.upper()

    return f'X:{sym.upper()}'


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
