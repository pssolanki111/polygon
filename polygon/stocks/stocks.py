# ========================================================= #
from .. import base_client
from os import cpu_count

# ========================================================= #


def StocksClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10,
                 pool_timeout: int = 10, max_connections: int = None, max_keepalive: int = None,
                 write_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST Stocks endpoints.

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
        return SyncStocksClient(api_key, connect_timeout, read_timeout)

    return AsyncStocksClient(api_key, connect_timeout, read_timeout, pool_timeout, max_connections,
                             max_keepalive, write_timeout)


# ========================================================= #


class SyncStocksClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Stocks REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import StocksClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    def get_trades(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                   limit: int = 5000, raw_response: bool = False):
        """
        Get trades for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_ticks_stocks_trades__ticker___date>`__

        :param symbol: The ticker symbol we want trades for.
        :param date: The date/day of the trades to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                          results. Using the ``timestamp`` of the last result as the offset will give you the next page
                          of results. Default: None. I'm trying to think of a good way to implement pagination
                          support for this type of pagination.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded 
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        timestamp = self.normalize_datetime(timestamp)

        _path = f'/v2/ticks/stocks/trades/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_trades_v3(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                      all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                      verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get trades for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_trades__stockticker>`__

        :param symbol: The ticker symbol you want trades for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksTradesSort` for
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

        _path = f'/v3/trades/{symbol}'

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

    @staticmethod
    def get_trades_vx(*args, **kwargs):
        print(f'This method has been removed as polygon changed this endpoint to v3 (yeah I don\'t like that behavior '
              f'either from polygon. Please use "get_trades_v3", you can use the exact same arguments. the function '
              f'did not change :)')

    @staticmethod
    def get_quotes_vx(*args, **kwargs):
        print(f'This method has been removed as polygon changed this endpoint to v3 (yeah I don\'t like that behavior '
              f'either from polygon. Please use "get_quotes_v3", you can use the exact same arguments. the function '
              f'did not change :)')

    def get_quotes(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                   limit: int = 5000, raw_response: bool = False):
        """
        Get Quotes for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_ticks_stocks_nbbo__ticker___date>`__

        :param symbol: The ticker symbol we want quotes for.
        :param date: The date/day of the quotes to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                         results. Using the ``timestamp`` of the last result as the offset will give you the next
                         page of results. Default: None. Thinking of a good way to implement this pagination here.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        timestamp = self.normalize_datetime(timestamp)

        _path = f'/v2/ticks/stocks/nbbo/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_quotes_v3(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                      all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                      verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get NBBO Quotes for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_quotes__stockticker>`__

        :param symbol: The ticker symbol you want quotes for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksQuotesSort` for
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

        _path = f'/v3/quotes/{symbol}'

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

    def get_last_trade(self, symbol: str, raw_response: bool = False):
        """
        Get the most recent trade for a given stock.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_trade__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/trade/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_last_quote(self, symbol: str, raw_response: bool = False):
        """
        Get the most recent NBBO (Quote) tick for a given stock.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_nbbo__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/nbbo/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_daily_open_close(self, symbol: str, date, adjusted: bool = True,
                             raw_response: bool = False):
        """
        Get the OCHLV and after-hours prices of a stock symbol on a certain date.
        `Official Docs <https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date>`__

        :param symbol: The ticker symbol we want daily-OCHLV for.
        :param date: The date/day of the daily-OCHLV to retrieve. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v1/open-close/{symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_aggregate_bars(self, symbol: str, from_date, to_date, adjusted: bool = True,
                           sort='asc', limit: int = 5000, multiplier: int = 1, timespan='day', full_range: bool = False,
                           run_parallel: bool = True, max_concurrent_workers: int = cpu_count() * 5,
                           warnings: bool = True, high_volatility: bool = False, raw_response: bool = False):
        """
        Get aggregate bars for a stock over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
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

            _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

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
    
    def get_full_range_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='min',
                                      adjusted: bool = True, sort='asc', run_parallel: bool = True, 
                                      max_concurrent_workers: int = cpu_count() * 5,
                                      warnings: bool = True, high_volatility: bool = False):
        """
        Get BULK full range aggregate bars (OCHLV candles) for a stock.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘1’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without prefix
                       ``X:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to minute candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
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
        :return: a single list with all the candles.
        """
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                  max_concurrent_workers, warnings, adjusted=adjusted,
                                                  multiplier=multiplier, sort=sort, limit=50_000,
                                                  timespan=timespan)

        # Sequential Run
        time_chunks = [from_date, to_date]
        return self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                              max_concurrent_workers, warnings, adjusted=adjusted,
                                              multiplier=multiplier, sort=sort, limit=50_000,
                                              timespan=timespan)

    def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False):
        """
        Get the daily OCHLV for the entire stocks/equities markets.
        `Official docs <https://polygon.io/docs/stocks/get_v2_aggs_grouped_locale_us_market_stocks__date>`__

        :param date: The date to get the data for. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v2/aggs/grouped/locale/us/market/stocks/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_previous_close(self, symbol: str, adjusted: bool = True,
                           raw_response: bool = False):
        """
        Get the previous day's OCHLV for the specified stock ticker.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__prev>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
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

    def get_snapshot(self, symbol: str, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded stock ticker.
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers/{symbol.upper()}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_current_price(self, symbol: str) -> float:
        """
        get current market price for the ticker symbol specified.

        Uses :meth:`get_last_trade` under the hood
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_trade__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :return: The current price. A ``KeyError`` indicates the request wasn't successful.
        """

        _res = self.get_last_trade(symbol)

        try:
            return _res['results']['p']
        except KeyError:
            raise ValueError('Request failed. Make sure your API key is correct and your subscription has access to '
                             f'the data you requested. Response from the API: {_res}')

    def get_snapshot_all(self, symbols: list = None, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        stock symbols.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers>`__

        :param symbols: A comma separated list of tickers to get snapshots for. Defaults to ALL tickers
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers'

        if symbols is not None:
            _data = {'tickers': ','.join([x.upper() for x in symbols])}
        else:
            _data = {'tickers': None}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_gainers_and_losers(self, direction='gainers', raw_response: bool = False):
        """
        Get the current top 20 gainers or losers of the day in stocks/equities markets.
        `Official Docs <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks__direction>`__

        :param direction: The direction of results. Defaults to gainers. See :class:`polygon.enums.SnapshotDirection`
                          for choices
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/{self._change_enum(direction, str)}'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()
    
    # Technical Indicators
    def get_sma(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 50,
                series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                raw_response: bool = False):
        """
        Get the Simple Moving Average for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the simple moving average are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the simple moving average (SMA). i.e. a window 
                            size of 10 with daily aggregates would result in a 10 day moving average.
        :param series_type: The prices in the aggregate which will be used to calculate the SMA. 
                            The default ``close`` will result in using close prices to calculate the SMA.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the SMA.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        return self._get_sma(symbol, timestamp, timespan, adjusted, window_size, series_type,
                             include_underlying, order, limit, timestamp_lt, timestamp_lte,
                             timestamp_gt, timestamp_gte, raw_response)
    
    def get_ema(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 50,
                series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                raw_response: bool = False):
        """
        Get the Exponential Moving Average for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the EMA are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the EMA. i.e. a window 
                            size of 10 with daily aggregates would result in a 10 day moving average.
        :param series_type: The prices in the aggregate which will be used to calculate the EMA. 
                            The default ``close`` will result in using close prices to calculate the EMA.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the EMA.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        return self._get_ema(symbol, timestamp, timespan, adjusted, window_size, series_type,
                             include_underlying, order, limit, timestamp_lt, timestamp_lte,
                             timestamp_gt, timestamp_gte, raw_response)
    
    def get_rsi(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 14,
                series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                raw_response: bool = False):
        """
        Get the Relative Strength Index for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the RSI are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the RSI. i.e. a window 
                            size of 14 with daily aggregates would result in a 14 day RSI.
        :param series_type: The prices in the aggregate which will be used to calculate the RSI. 
                            The default ``close`` will result in using close prices to calculate the RSI.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the RSI.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        return self._get_rsi(symbol, timestamp, timespan, adjusted, window_size, series_type,
                             include_underlying, order, limit, timestamp_lt, timestamp_lte,
                             timestamp_gt, timestamp_gte, raw_response)
    
    def get_macd(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, long_window_size: int = 50,
                 series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                 timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                 short_window_size: int = 50, signal_window_size: int = 50,
                 raw_response: bool = False):
        """
        Get the Moving Average Convergence/Divergence for a stock

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the MACD are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that are NOT 
                         adjusted for splits.
        :param long_window_size: The long window size used to calculate the MACD data
        :param series_type: The prices in the aggregate which will be used to calculate the MACD. 
                            The default ``close`` will result in using close prices to calculate the MACD.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the MACD.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :param short_window_size: The short window size used to calculate the MACD data
        :param signal_window_size: The window size used to calculate the MACD signal line.
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        return self._get_macd(symbol, timestamp, timespan, adjusted, long_window_size, series_type, 
                              include_underlying, order, limit, timestamp_lt, timestamp_lte, timestamp_gt, 
                              timestamp_gte, short_window_size, signal_window_size, raw_response)


# ========================================================= #


class AsyncStocksClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Stocks REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import StocksClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10, pool_timeout: int = 10,
                 max_connections: int = None, max_keepalive: int = None, write_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout, pool_timeout, max_connections, max_keepalive,
                         write_timeout)

    # Endpoints
    async def get_trades(self, symbol: str, date,
                         timestamp: int = None, timestamp_limit: int = None, reverse: bool = True,
                         limit: int = 5000, raw_response: bool = False):
        """
        Get trades for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_ticks_stocks_trades__ticker___date>`__

        :param symbol: The ticker symbol we want trades for.
        :param date: The date/day of the trades to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                          results. Using the ``timestamp`` of the last result as the offset will give you the next page
                          of results. Default: None. I'm trying to think of a good way to implement pagination
                          support for this type of pagination.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        timestamp = self.normalize_datetime(timestamp)

        _path = f'/v2/ticks/stocks/trades/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_trades_v3(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                            timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                            all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                            verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get trades for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_trades__stockticker>`__

        :param symbol: The ticker symbol you want trades for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksTradesSort` for
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

        _path = f'/v3/trades/{symbol}'

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

    @staticmethod
    async def get_trades_vx(*args, **kwargs):
        print(f'This method has been removed as polygon changed this endpoint to v3 (yeah I don\'t like that behavior '
              f'either from polygon. Please use "get_trades_v3", you can use the exact same arguments. the function '
              f'did not change :)')

    @staticmethod
    async def get_quotes_vx(*args, **kwargs):
        print(f'This method has been removed as polygon changed this endpoint to v3 (yeah I don\'t like that behavior '
              f'either from polygon. Please use "get_quotes_v3", you can use the exact same arguments. the function '
              f'did not change :)')

    async def get_quotes(self, symbol: str, date, timestamp: int = None, timestamp_limit: int = None,
                         reverse: bool = True, limit: int = 5000,
                         raw_response: bool = False):
        """
        Get Quotes for a given ticker symbol on a specified date. The response from polygon seems to have a ``map``
        attribute which gives a mapping of attribute names to readable values - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_ticks_stocks_nbbo__ticker___date>`__

        :param symbol: The ticker symbol we want quotes for.
        :param date: The date/day of the quotes to retrieve. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param timestamp: The timestamp offset, used for pagination. Timestamp is the offset at which to start the
                         results. Using the ``timestamp`` of the last result as the offset will give you the next
                         page of results. Default: None. Thinking of a good way to implement this pagination here.
        :param timestamp_limit: The maximum timestamp allowed in the results. Default: None
        :param reverse: Reverse the order of the results. Default True: oldest first. Make it False for Newest first
        :param limit: Limit the size of the response, max 50000 and default 5000.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')
        timestamp = self.normalize_datetime(timestamp)

        _path = f'/v2/ticks/stocks/nbbo/{symbol.upper()}/{date}'

        _data = {'timestamp': timestamp,
                 'timestampimit': timestamp_limit,
                 'reverse': 'true' if reverse else 'false',
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_quotes_v3(self, symbol: str, timestamp: int = None, order=None, sort=None, limit: int = 5000,
                            timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None,
                            all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                            verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get NBBO Quotes for a ticker symbol in a given time range.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_quotes__stockticker>`__

        :param symbol: The ticker symbol you want quotes for.
        :param timestamp: Query by trade timestamp. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD`` or a
                          nanosecond timestamp
        :param order: sort order. see :class:`polygon.enums.SortOrder` for available choices. defaults to None
        :param sort: field key to sort against. Defaults to None. see :class:`polygon.enums.StocksQuotesSort` for
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

        _path = f'/v3/quotes/{symbol}'

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

    async def get_last_trade(self, symbol: str, raw_response: bool = False):
        """
        Get the most recent trade for a given stock - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_trade__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/trade/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_last_quote(self, symbol: str, raw_response: bool = False):
        """
        Get the most recent NBBO (Quote) tick for a given stock - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_nbbo__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/last/nbbo/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_daily_open_close(self, symbol: str, date, adjusted: bool = True,
                                   raw_response: bool = False):
        """
        Get the OCHLV and after-hours prices of a stock symbol on a certain date - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v1_open-close__stocksticker___date>`__

        :param symbol: The ticker symbol we want daily-OCHLV for.
        :param date: The date/day of the daily-OCHLV to retrieve. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v1/open-close/{symbol.upper()}/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_aggregate_bars(self, symbol: str, from_date, to_date, adjusted: bool = True,
                                 sort='asc', limit: int = 5000, multiplier: int = 1, timespan='day',
                                 full_range: bool = False, run_parallel: bool = True,
                                 max_concurrent_workers: int = cpu_count() * 5,  warnings: bool = True,
                                 high_volatility: bool = False, raw_response: bool = False):
        """
        Get aggregate bars for a stock over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
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

            _path = f'/v2/aggs/ticker/{symbol.upper()}/range/{multiplier}/{timespan}/{from_date}/{to_date}'

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
    
    async def get_full_range_aggregate_bars(self, symbol: str, from_date, to_date, multiplier: int = 1, timespan='min',
                                            adjusted: bool = True, sort='asc', run_parallel: bool = True, 
                                            max_concurrent_workers: int = cpu_count() * 5,
                                            warnings: bool = True, high_volatility: bool = False):
        """
        Get BULK full range aggregate bars (OCHLV candles) for a stock.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘1’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the currency pair. eg: ``X:BTCUSD``. You can specify with or without prefix
                       ``X:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to minute candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param adjusted: Whether the results are adjusted for splits. By default, results are adjusted.
                         Set this to False to get results that are NOT adjusted for splits.
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
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
        :return: a single list with all the candles.
        """
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return await self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                        max_concurrent_workers, warnings, adjusted=adjusted,
                                                        multiplier=multiplier, sort=sort, limit=50_000,
                                                        timespan=timespan)

        # Sequential Run
        time_chunks = [from_date, to_date]
        return await self.get_full_range_aggregates(self.get_aggregate_bars, symbol, time_chunks, run_parallel,
                                                    max_concurrent_workers, warnings, adjusted=adjusted,
                                                    multiplier=multiplier, sort=sort, limit=50_000,
                                                    timespan=timespan)

    async def get_grouped_daily_bars(self, date, adjusted: bool = True, raw_response: bool = False):
        """
        Get the daily OCHLV for the entire stocks/equities markets - Async method
        `Official docs <https://polygon.io/docs/stocks/get_v2_aggs_grouped_locale_us_market_stocks__date>`__

        :param date: The date to get the data for. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v2/aggs/grouped/locale/us/market/stocks/{date}'

        _data = {'adjusted': 'true' if adjusted else 'false'}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_previous_close(self, symbol: str, adjusted: bool = True,
                                 raw_response: bool = False):
        """
        Get the previous day's OCHLV for the specified stock ticker - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__prev>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this
                         to false to get results that are NOT adjusted for splits.
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

    async def get_snapshot(self, symbol: str, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single
        traded stock ticker - Async method
        `Official Docs
        <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers/{symbol.upper()}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_current_price(self, symbol: str) -> float:
        """
        get current market price for the ticker symbol specified - Async method

        Uses :meth:`get_last_trade` under the hood
        `Official Docs <https://polygon.io/docs/stocks/get_v2_last_trade__stocksticker>`__

        :param symbol: The ticker symbol of the stock/equity.
        :return: The current price. A ``KeyError`` indicates the request wasn't successful.
        """

        _res = await self.get_last_trade(symbol)

        return _res['results']['p']

    async def get_snapshot_all(self, symbols: list = None, raw_response: bool = False):
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for all traded
        stock symbols - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers>`__

        :param symbols: A comma separated list of tickers to get snapshots for. Defaults to ALL tickers
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/tickers'

        if symbols is not None:
            _data = {'tickers': ','.join([x.upper() for x in symbols])}
        else:
            _data = {'tickers': None}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_gainers_and_losers(self, direction='gainers',
                                     raw_response: bool = False):
        """
        Get the current top 20 gainers or losers of the day in stocks/equities markets - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_snapshot_locale_us_markets_stocks__direction>`__

        :param direction: The direction of results. Defaults to gainers. See :class:`polygon.enums.SnapshotDirection`
                          for choices
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f'/v2/snapshot/locale/us/markets/stocks/{self._change_enum(direction, str)}'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    # Technical Indicators
    async def get_sma(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 50,
                      series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None):
        """
        Get the Simple Moving Average for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the simple moving average are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that 
                         are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the simple moving average (SMA). i.e. a window 
                            size of 10 with daily aggregates would result in a 10 day moving average.
        :param series_type: The prices in the aggregate which will be used to calculate the SMA. 
                            The default ``close`` will result in using close prices to calculate the SMA.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the SMA.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :return: The response object
        """
        return await self._get_sma(symbol, timestamp, timespan, adjusted, window_size, series_type,
                                   include_underlying, order, limit, timestamp_lt, timestamp_lte,
                                   timestamp_gt, timestamp_gte)

    async def get_ema(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 50,
                      series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None):
        """
        Get the Exponential Moving Average for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the EMA are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that 
                         are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the EMA. i.e. a window 
                            size of 10 with daily aggregates would result in a 10 day moving average.
        :param series_type: The prices in the aggregate which will be used to calculate the EMA. 
                            The default ``close`` will result in using close prices to calculate the EMA.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the EMA.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :return: The response object
        """
        return await self._get_ema(symbol, timestamp, timespan, adjusted, window_size, series_type,
                                   include_underlying, order, limit, timestamp_lt, timestamp_lte,
                                   timestamp_gt, timestamp_gte)

    async def get_rsi(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True, window_size: int = 14,
                      series_type='close', include_underlying: bool = False, order='desc', limit: int = 5000,
                      timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, timestamp_gte=None):
        """
        Get the Relative Strength Index for a Stock symbol

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the RSI are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that 
                         are NOT 
                         adjusted for splits.
        :param window_size: The window size used to calculate the RSI. i.e. a window 
                            size of 14 with daily aggregates would result in a 14 day RSI.
        :param series_type: The prices in the aggregate which will be used to calculate the RSI. 
                            The default ``close`` will result in using close prices to calculate the RSI.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the RSI.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :return: The response object
        """
        return await self._get_rsi(symbol, timestamp, timespan, adjusted, window_size, series_type,
                                   include_underlying, order, limit, timestamp_lt, timestamp_lte,
                                   timestamp_gt, timestamp_gte)

    async def get_macd(self, symbol: str, timestamp=None, timespan='day', adjusted: bool = True,
                       long_window_size: int = 50, series_type='close', include_underlying: bool = False, 
                       order='desc', limit: int = 5000, timestamp_lt=None, timestamp_lte=None, timestamp_gt=None, 
                       timestamp_gte=None, short_window_size: int = 50, signal_window_size: int = 50):
        """
        Get the Moving Average Convergence/Divergence for a stock

        :param symbol: The stock symbol
        :param timestamp: Either a date with the format ``YYYY-MM-DD`` or a millisecond timestamp.
        :param timespan: Size of the aggregate time window. defaults to 'day'. See :class:`polygon.enums.Timespan` 
                         for choices
        :param adjusted: Whether the aggregates used to calculate the MACD are adjusted for 
                         splits. By default, aggregates are adjusted. Set this to ``False`` to get results that 
                         are NOT 
                         adjusted for splits.
        :param long_window_size: The long window size used to calculate the MACD data
        :param series_type: The prices in the aggregate which will be used to calculate the MACD. 
                            The default ``close`` will result in using close prices to calculate the MACD.
                            See :class:`polygon.enums.SeriesType` for choices
        :param include_underlying: Whether to include the OCHLV aggregates used to calculate this 
                                   indicator in the response. Defaults to False which only returns the MACD.
        :param order: The order in which to return the results, ordered by timestamp. 
                      See :class:`polygon.enums.SortOrder` for choices. Defaults to Descending (most recent first) 
        :param limit: Limit the number of results returned, default is 5000 which is also the max
        :param timestamp_lt: Only use results where timestamp is less than supplied value
        :param timestamp_lte: Only use results where timestamp is less than or equal to supplied value
        :param timestamp_gt: Only use results where timestamp is greater than supplied value
        :param timestamp_gte: Only use results where timestamp is greater than or equal to supplied value
        :param short_window_size: The short window size used to calculate the MACD data
        :param signal_window_size: The window size used to calculate the MACD signal line.
        :return: The response object
        """
        return await self._get_macd(symbol, timestamp, timespan, adjusted, long_window_size, series_type,
                                    include_underlying, order, limit, timestamp_lt, timestamp_lte, timestamp_gt,
                                    timestamp_gte, short_window_size, signal_window_size)


# ========================================================= #


if __name__ == '__main__':  # Tests
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
