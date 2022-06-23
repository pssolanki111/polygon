# ========================================================= #
from .. import base_client
from typing import Union
from os import cpu_count

# ========================================================= #


def ForexClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10,
                pool_timeout: int = 10, max_connections: int = None, max_keepalive: int = None,
                write_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST Forex endpoints.

    :param api_key: Your API Key. Visit your dashboard to get yours.
    :param use_async: Set it to ``True`` to get async client. Defaults to usual non-async client.
    :param connect_timeout: The connection timeout in seconds. Defaults to 10. basically the number of seconds to
                            wait for a connection to be established. Raises a ``ConnectTimeout`` if unable to
                            connect within specified time limit.
    :param read_timeout: The read timeout in seconds. Defaults to 10. basically the number of seconds to wait for
                         date to be received. Raises a ``ReadTimeout`` if unable to connect within the specified
                         time limit.
    :param pool_timeout: The pool timeout in seconds. Defaults to 10. Basically the number of seconds to wait while
                             trying to get a connection from connection pool. Do NOT change if you're unsure of what it
                             implies
    :param max_connections: Max number of connections in the pool. Defaults to NO LIMITS. Do NOT change if you're
                            unsure of application
    :param max_keepalive: max number of allowable keep alive connections in the pool. Defaults to no limit.
                          Do NOT change if you're unsure of the applications.
    :param write_timeout: The write timeout in seconds. Defaults to 10. basically the number of seconds to wait for
                         data to be written/posted. Raises a ``WriteTimeout`` if unable to connect within the
                         specified time limit.
    """

    if not use_async:
        return SyncForexClient(api_key, connect_timeout, read_timeout)

    return AsyncForexClient(api_key, connect_timeout, read_timeout, pool_timeout, max_connections,
                            max_keepalive, write_timeout)


# ========================================================= #


class SyncForexClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Forex REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ForexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    def get_historic_forex_ticks(self, from_symbol: str, to_symbol: str, date, offset: Union[str, int] = None,
                                 limit: int = 500, raw_response: bool = False):
        """
        Get historic trade ticks for a forex currency pair.
        `Official Docs <https://polygon.io/docs/forex/get_v1_historic_forex__from___to___date>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string 
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm thinking about a good way to implement this type of pagination in the lib which doesn't 
                       have a ``next_url`` in the response attributes.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        offset = self.normalize_datetime(offset)

        _path = f'/v1/historic/forex/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_quotes(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                   timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                   all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                   verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get NBBO Quotes for a forex ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/forex/get_v3_quotes__fxticker>`__

        :param symbol: The ticker symbol you want quotes for. eg: ``C:EUR-USD``. you can pass with or without prefix C:
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.ForexQuotesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string or
                             nanosecond timestamp
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string or nanosecond timestamp
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string or nanosecond timestamp
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string or nanosecond timestamp
        :param all_pages: Whether to paginate through next/previous pages internally. Defaults to False. If set to True,
                          it will try to paginate through all pages and merge all pages internally for you.
        :param max_pages: how many pages to fetch. Defaults to None which fetches all available pages. Change to an
                          integer to fetch at most that many pages. This param is only considered if ``all_pages``
                          is set to True
        :param merge_all_pages: If this is True, returns a single merged response having all the data. If False,
                                returns a list of all pages received. The list can be either a list of response
                                objects or decoded data itself, controlled by parameter ``raw_page_responses``.
                                This argument is Only considered if ``all_pages`` is set to True. Default: True
        :param verbose: Set to True to print status messages during the pagination process. Defaults to False.
        :param raw_page_responses: If this is true, the list of pages will be a list of corresponding Response objects.
                                   Else, it will be a list of actual data for pages. This parameter is only
                                   considered if ``merge_all_pages`` is set to False. Default: False
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """

        timestamp = self.normalize_datetime(timestamp, output_type='nts', unit='ns')

        timestamp_lt = self.normalize_datetime(timestamp_lt, output_type='nts', unit='ns')

        timestamp_lte = self.normalize_datetime(timestamp_lte, output_type='nts', unit='ns')

        timestamp_gt = self.normalize_datetime(timestamp_gt, output_type='nts', unit='ns')

        timestamp_gte = self.normalize_datetime(timestamp_gte, output_type='nts', unit='ns')

        _path = f'/v3/quotes/{ensure_prefix(symbol)}'

        _data = {'timestamp': timestamp, 'timestamp.lt': timestamp_lt, 'timestamp.lte': timestamp_lte,
                 'timestamp.gt': timestamp_gt, 'timestamp.gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_last_quote(self, from_symbol: str, to_symbol: str, raw_response: bool = False):
        """
        Get the last trade tick for a forex currency pair.
        `Official Docs <hhttps://polygon.io/docs/forex/get_v1_last_quote_currencies__from___to>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last_quote/currencies/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='day',
                           adjusted: bool = True, sort='asc', limit: int = 5000, full_range: bool = False,
                           run_parallel: bool = True, max_concurrent_workers: int = cpu_count() * 5,
                           warnings: bool = True, high_volatility: bool = False, raw_response: bool = False):
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then ``5-minute`` bars will be returned.
        `Official Docs
        <https://polygon.io/docs/forex/get_v2_aggs_ticker__forexticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix 
                       ``C:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string 
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. see :class:`polygon.enums.SortOrder` for available choices. 
                     Defaults to ``asc`` which is oldest at the top.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param full_range: Default False. If set to True, it will get the ENTIRE range you specify and **merge** all
                           the responses and return ONE single list with all data in it. You can control its behavior
                           with the next few arguments.
        :param run_parallel: Only considered if ``full_range=True``. If set to true (default True), it will run an
                             internal ThreadPool to get the responses. This is fine to do if you are not running your
                             own ThreadPool. If you have many tickers to get aggs for, it's better to either use the
                             async version of it OR set this to False and spawn threads for each ticker yourself.
        :param max_concurrent_workers: Only considered if ``run_parallel=True``. Defaults to ``your cpu cores * 5``.
                                       controls how many worker threads to use in internal ThreadPool
        :param warnings: Set to False to disable printing warnings if any when fetching the aggs. Defaults to True.
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (eg SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. Will be ignored if ``full_range=True``
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If ``full_range=True``, will return a single list with all the candles in it.
        """

        if not full_range:

            from_date = self.normalize_datetime(from_date, output_type='nts')

            to_date = self.normalize_datetime(to_date, output_type='nts', _dir='end')

            if timespan == 'min':
                timespan = 'minute'

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

        # The full range agg begins
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                  max_concurrent_workers, warnings, adjusted=adjusted,
                                                  multiplier=multiplier, sort=sort, limit=limit,
                                                  timespan=timespan)

        # Sequential Run
        time_chunks = [from_date, to_date]
        return self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                              max_concurrent_workers, warnings, adjusted=adjusted,
                                              multiplier=multiplier, sort=sort, limit=limit,
                                              timespan=timespan)

    def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False):
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets.
        `Official Docs <https://polygon.io/docs/forex/get_v2_aggs_grouped_locale_global_market_fx__date>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v2/aggs/grouped/locale/global/market/fx/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False):
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified forex pair.
        `Official Docs <https://polygon.io/docs/forex/get_v2_aggs_ticker__forexticker__prev>`__

        :param symbol: The ticker symbol of the forex pair.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{symbol.upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot_all(self, symbols: list, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        forex symbols
        `Official Docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_snapshot(self, symbol: str, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded forex symbol.
        `Official Docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers__ticker>`__

        :param symbol: Symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix ``C:``.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{ensure_prefix(symbol).upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction='gainers', raw_response: bool = False):
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        `Official docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex__direction>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/{direction}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def real_time_currency_conversion(self, from_symbol: str, to_symbol: str, amount: float, precision: int = 2,
                                      raw_response: bool = False):
        """
        Get currency conversions using the latest market conversion rates. Note than you can convert in both directions.
        For example USD to CAD or CAD to USD.
        `Official Docs <https://polygon.io/docs/forex/get_v1_conversion__from___to>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param amount: The amount to convert,
        :param precision: The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/conversion/{from_symbol.upper()}/{to_symbol.upper()}'

        _data = {'amount': amount,
                 'precision': precision}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


class AsyncForexClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Forex REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ForexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10, pool_timeout: int = 10,
                 max_connections: int = None, max_keepalive: int = None, write_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout, pool_timeout, max_connections, max_keepalive,
                         write_timeout)

    # Endpoints
    async def get_historic_forex_ticks(self, from_symbol: str, to_symbol: str,
                                       date, offset: Union[str, int] = None, limit: int = 500,
                                       raw_response: bool = False):
        """
        Get historic trade ticks for a forex currency pair - Async method.
        `Official Docs <https://polygon.io/docs/forex/get_v1_historic_forex__from___to___date>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param date: The date/day of the historic ticks to retrieve. Could be ``datetime``, ``date`` or string
                     ``YYYY-MM-DD``
        :param offset: The timestamp offset, used for pagination. This is the offset at which to start the results.
                       Using the timestamp of the last result as the offset will give you the next page of results.
                       I'm thinking about a good way to implement this type of pagination in the lib which doesn't
                       have a ``next_url`` in the response attributes.
        :param limit: Limit the size of the response, max 10000. Default 500
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        offset = self.normalize_datetime(offset)

        _path = f'/v1/historic/forex/{from_symbol.upper()}/{to_symbol.upper()}/{date}'

        _data = {'offset': offset,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_quotes(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                         timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                         all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                         verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get NBBO Quotes for a forex ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/forex/get_v3_quotes__fxticker>`__

        :param symbol: The ticker symbol you want quotes for. eg: ``C:EUR-USD``. you can pass with or without prefix C:
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.ForexQuotesSort` for
                     choices
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param timestamp_lt: return results where timestamp is less than the given value. Can be date or date string or
                             nanosecond timestamp
        :param timestamp_lte: return results where timestamp is less than/equal to the given value. Can be date or date
                              string or nanosecond timestamp
        :param timestamp_gt: return results where timestamp is greater than the given value. Can be date or date
                             string or nanosecond timestamp
        :param timestamp_gte: return results where timestamp is greater than/equal to the given value. Can be date or
                              date string or nanosecond timestamp
        :param all_pages: Whether to paginate through next/previous pages internally. Defaults to False. If set to True,
                          it will try to paginate through all pages and merge all pages internally for you.
        :param max_pages: how many pages to fetch. Defaults to None which fetches all available pages. Change to an
                          integer to fetch at most that many pages. This param is only considered if ``all_pages``
                          is set to True
        :param merge_all_pages: If this is True, returns a single merged response having all the data. If False,
                                returns a list of all pages received. The list can be either a list of response
                                objects or decoded data itself, controlled by parameter ``raw_page_responses``.
                                This argument is Only considered if ``all_pages`` is set to True. Default: True
        :param verbose: Set to True to print status messages during the pagination process. Defaults to False.
        :param raw_page_responses: If this is true, the list of pages will be a list of corresponding Response objects.
                                   Else, it will be a list of actual data for pages. This parameter is only
                                   considered if ``merge_all_pages`` is set to False. Default: False
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """

        timestamp = self.normalize_datetime(timestamp, output_type='nts', unit='ns')

        timestamp_lt = self.normalize_datetime(timestamp_lt, output_type='nts', unit='ns')

        timestamp_lte = self.normalize_datetime(timestamp_lte, output_type='nts', unit='ns')

        timestamp_gt = self.normalize_datetime(timestamp_gt, output_type='nts', unit='ns')

        timestamp_gte = self.normalize_datetime(timestamp_gte, output_type='nts', unit='ns')

        _path = f'/v3/quotes/{ensure_prefix(symbol)}'

        _data = {'timestamp': timestamp, 'timestamp.lt': timestamp_lt, 'timestamp.lte': timestamp_lte,
                 'timestamp.gt': timestamp_gt, 'timestamp.gte': timestamp_gte, 'limit': limit,
                 'sort': self._change_enum(sort, str), 'order': self._change_enum(order, str)}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_last_quote(self, from_symbol: str, to_symbol: str,
                             raw_response: bool = False):
        """
        Get the last trade tick for a forex currency pair - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v1_last_quote_currencies__from___to>`__

        :param from_symbol: The "from" symbol of the forex currency pair.
        :param to_symbol: The "to" symbol of the forex currency pair.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/last_quote/currencies/{from_symbol.upper()}/{to_symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='day',
                                 adjusted: bool = True, sort='asc', limit: int = 5000, full_range: bool = False,
                                 run_parallel: bool = True, max_concurrent_workers: int = cpu_count() * 5,
                                 warnings: bool = True, high_volatility: bool = False, raw_response: bool = False):
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then ``5-minute`` bars will be returned.
        `Official Docs
        <https://polygon.io/docs/forex/get_v2_aggs_ticker__forexticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix
                       ``C:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to day candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. see :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` which is oldest at the top.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param full_range: Default False. If set to True, it will get the ENTIRE range you specify and **merge** all
                           the responses and return ONE single list with all data in it. You can control its behavior
                           with the next few arguments.
        :param run_parallel: Only considered if ``full_range=True``. If set to true (default True), it will run an
                             internal ThreadPool to get the responses. This is fine to do if you are not running your
                             own ThreadPool. If you have many tickers to get aggs for, it's better to either use the
                             async version of it OR set this to False and spawn threads for each ticker yourself.
        :param max_concurrent_workers: Only considered if ``run_parallel=True``. Defaults to ``your cpu cores * 5``.
                                       controls how many worker threads to use in internal ThreadPool
        :param warnings: Set to False to disable printing warnings if any when fetching the aggs. Defaults to True.
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (eg SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. Will be ignored if ``full_range=True``
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If ``full_range=True``, will return a single list with all the candles in it.
        """

        if not full_range:

            from_date = self.normalize_datetime(from_date, output_type='nts')

            to_date = self.normalize_datetime(to_date, output_type='nts', _dir='end')

            if timespan == 'min':
                timespan = 'minute'

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

        # The full range agg begins
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return await self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                        max_concurrent_workers, warnings, adjusted=adjusted,
                                                        multiplier=multiplier, sort=sort, limit=limit,
                                                        timespan=timespan)

        # Sequential Run
        time_chunks = [from_date, to_date]
        return await self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                    max_concurrent_workers, warnings, adjusted=adjusted,
                                                    multiplier=multiplier, sort=sort, limit=limit,
                                                    timespan=timespan)

    async def get_grouped_daily_bars(self, date, adjusted: bool = True,
                                     raw_response: bool = False):
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v2_aggs_grouped_locale_global_market_fx__date>`__

        :param date: The date for the aggregate window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param adjusted:  Whether or not the results are adjusted for splits. By default, results are adjusted. Set
                          this to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v2/aggs/grouped/locale/global/market/fx/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_previous_close(self, symbol: str, adjusted: bool = True,
                                 raw_response: bool = False):
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified forex pair - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v2_aggs_ticker__forexticker__prev>`__

        :param symbol: The ticker symbol of the forex pair.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to False to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/aggs/ticker/{symbol.upper()}/prev'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot_all(self, symbols: list, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        forex symbols - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers>`__

        :param symbols: A list of tickers to get snapshots for.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        if not isinstance(symbols, list):
            raise ValueError('symbols must be supplied as a list of tickers')

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers'

        _data = {'tickers': ','.join([x.upper() for x in symbols])}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_snapshot(self, symbol: str, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded forex symbol - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers__ticker>`__

        :param symbol: Symbol of the forex pair. eg: ``C:EURUSD``. You can supply with or without prefix ``C:``.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/tickers/{ensure_prefix(symbol).upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_gainers_and_losers(self, direction='gainers',
                                     raw_response: bool = False):
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        `Official docs <https://polygon.io/docs/forex/get_v2_snapshot_locale_global_markets_forex__direction>`__

        :param direction: The direction of the snapshot results to return. See :class:`polygon.enums.SnapshotDirection`
                          for available choices. Defaults to Gainers.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/global/markets/forex/{direction}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def real_time_currency_conversion(self, from_symbol: str, to_symbol: str, amount: float,
                                            precision: int = 2,
                                            raw_response: bool = False):
        """
        Get currency conversions using the latest market conversion rates. Note than you can convert in both directions.
        For example USD to CAD or CAD to USD - Async method
        `Official Docs <https://polygon.io/docs/forex/get_v1_conversion__from___to>`__

        :param from_symbol: The "from" symbol of the pair.
        :param to_symbol: The "to" symbol of the pair.
        :param amount: The amount to convert,
        :param precision: The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v1/conversion/{from_symbol.upper()}/{to_symbol.upper()}'

        _data = {'amount': amount,
                 'precision': precision}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


def ensure_prefix(sym: str):
    if sym.upper().startswith('C:'):
        return sym.upper()

    return f'C:{sym.upper()}'


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
