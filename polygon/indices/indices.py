# ========================================================= #
from os import cpu_count

from .. import base_client


# ========================================================= #


def IndexClient(
    api_key: str,
    use_async: bool = False,
    connect_timeout: int = 10,
    read_timeout: int = 10,
    pool_timeout: int = 10,
    max_connections: int = None,
    max_keepalive: int = None,
    write_timeout: int = 10,
):
    """
    Initiates a Client to be used to access all REST Index endpoints.

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
        return SyncIndexClient(api_key, connect_timeout, read_timeout)

    return AsyncIndexClient(
        api_key, connect_timeout, read_timeout, pool_timeout, max_connections, max_keepalive, write_timeout
    )


# ========================================================= #


class SyncIndexClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Index REST endpoints. Note that you should always import names from top level.
    e.g.: ``from polygon import IndexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    def get_previous_close(self, symbol: str, raw_response: bool = False):
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified index.
        `Official Docs <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__prev>`__

        :param symbol: The ticker symbol of index (with or without the prefix `I:`)
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        _path = f"/v2/aggs/ticker/{ensure_prefix(symbol)}/prev"
        _data = {}

        _res = self._get_response(_path, params=_data)
        if raw_response:
            return _res

        return self.to_json_safe(_res)

    def get_daily_open_close(self, symbol: str, date, raw_response: bool = False):
        """
        Get the open, close and afterhours values of an index symbol on a certain date.
        `Official Docs <https://polygon.io/docs/indices/get_v1_open-close__indicesticker___date>`__

        :param symbol: The ticker symbol of index (with or without the prefix `I:`)
        :param date: The date/day for which to retrieve the data. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        date = self.normalize_datetime(date, output_type="str")
        _path = f"/v1/open-close/{ensure_prefix(symbol)}/{date}"
        _data = {}

        _res = self._get_response(_path, params=_data)
        if raw_response:
            return _res

        return self.to_json_safe(_res)

    def get_aggregate_bars(
        self,
        symbol: str,
        from_date,
        to_date,
        sort="asc",
        limit: int = 5000,
        multiplier: int = 1,
        timespan="day",
        adjusted: bool = False,
        full_range: bool = False,
        run_parallel: bool = True,
        max_concurrent_workers: int = cpu_count() * 5,
        warnings: bool = True,
        info: bool = True,
        high_volatility: bool = False,
        raw_response: bool = False,
    ):
        """
        Get aggregate bars for an index over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the Index.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
        :param adjusted: NOT applicable on Indices. Changing this will have NO IMPACT.
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
        :param info: Set to False to disable printing mild warnings / informational messages if any when fetching the
                     aggs. E.g. if there was no data in a response but the response had an OK status
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (e.g. SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. Will be ignored if ``full_range=True``
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If ``full_range=True``, will return a single list with all the candles in it.
        """

        if not full_range:
            from_date = self.normalize_datetime(from_date, output_type="nts")

            to_date = self.normalize_datetime(to_date, output_type="nts", _dir="end")

            if timespan == "min":
                timespan = "minute"

            timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

            _path = f"/v2/aggs/ticker/{ensure_prefix(symbol)}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

            _data = {"sort": sort, "limit": limit}

            _res = self._get_response(_path, params=_data)

            if raw_response:
                return _res

            return self.to_json_safe(_res)

        # The full range agg begins
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return self.get_full_range_aggregates(
                self.get_aggregate_bars,
                symbol,
                time_chunks,
                run_parallel,
                max_concurrent_workers,
                warnings,
                info=info,
                adjusted=adjusted,
                multiplier=multiplier,
                sort=sort,
                limit=limit,
                timespan=timespan,
            )

        # Sequential Run
        time_chunks = [from_date, to_date]
        return self.get_full_range_aggregates(
            self.get_aggregate_bars,
            symbol,
            time_chunks,
            run_parallel,
            max_concurrent_workers,
            warnings,
            info=info,
            adjusted=adjusted,
            multiplier=multiplier,
            sort=sort,
            limit=limit,
            timespan=timespan,
        )

    def get_full_range_aggregate_bars(
        self,
        symbol: str,
        from_date,
        to_date,
        multiplier: int = 1,
        timespan="min",
        sort="asc",
        adjusted: bool = False,
        run_parallel: bool = True,
        max_concurrent_workers: int = cpu_count() * 5,
        warnings: bool = True,
        info: bool = True,
        high_volatility: bool = False,
    ):
        """
        Get BULK full range aggregate bars (OCHLV candles) for an Index.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘1’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the Index. e.g.: ``I:NDX``. You can specify with or without prefix
                       ``I:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to minute candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
        :param adjusted: NOT applicable on Indices. Changing this will have NO IMPACT.
        :param run_parallel: Only considered if ``full_range=True``. If set to true (default True), it will run an
                             internal ThreadPool to get the responses. This is fine to do if you are not running your
                             own ThreadPool. If you have many tickers to get aggs for, it's better to either use the
                             async version of it OR set this to False and spawn threads for each ticker yourself.
        :param max_concurrent_workers: Only considered if ``run_parallel=True``. Defaults to ``your cpu cores * 5``.
                                       controls how many worker threads to use in internal ThreadPool
        :param warnings: Set to False to disable printing warnings if any when fetching the aggs. Defaults to True.
        :param info: Set to False to disable printing mild warnings / informational messages if any when fetching the
                     aggs. E.g. if there was no data in a response but the response had an OK status
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (e.g. SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :return: a single list with all the candles.
        """
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return self.get_full_range_aggregates(
                self.get_aggregate_bars,
                symbol,
                time_chunks,
                run_parallel,
                max_concurrent_workers,
                warnings,
                info=info,
                adjusted=adjusted,
                multiplier=multiplier,
                sort=sort,
                limit=50_000,
                timespan=timespan,
            )

        # Sequential Run
        time_chunks = [from_date, to_date]
        return self.get_full_range_aggregates(
            self.get_aggregate_bars,
            symbol,
            time_chunks,
            run_parallel,
            max_concurrent_workers,
            warnings,
            info=info,
            adjusted=adjusted,
            multiplier=multiplier,
            sort=sort,
            limit=50_000,
            timespan=timespan,
        )

    def get_snapshot(
        self,
        symbols: list = None,
        order="desc",
        limit: int = 5000,
        sort="ticker",
        ticker_lt: str = None,
        ticker_lte: str = None,
        ticker_gt: str = None,
        ticker_gte: str = None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get a Snapshot of indices data for said tickers
        `Official Docs <https://polygon.io/docs/indices/get_v3_snapshot_indices>`__

        :param symbols: list of Index tickers, up to a maximum of 250. Defaults to ALL tickers
        :param ticker_lt: Return results where this field is less than the value given
        :param ticker_lte: Return results where this field is less than or equal to the value given
        :param ticker_gt: Return results where this field is greater than the value given
        :param ticker_gte: Return results where this field is greater than or equal to the value given
        :param sort: Sort field key used for ordering. 'ticker' default. see
                     :class:`polygon.enums.IndexSnapshotSortKey` for choices.
        :param order: The order to sort the results on. Default is asc. See :class:`polygon.enums.SortOrder` for
                      available choices.
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
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
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f"/v3/snapshot/indices"

        if symbols is not None:
            tickers = ",".join([ensure_prefix(x) for x in symbols])
        else:
            tickers = None

        _data = {
            "ticker.any_of": tickers,
            "ticker.lt": ticker_lt,
            "ticker.lte": ticker_lte,
            "ticker.gt": ticker_gt,
            "ticker.gte": ticker_gte,
            "limit": limit,
            "sort": self._change_enum(sort, str),
            "order": self._change_enum(order, str),
        }

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginate!!
            if raw_response:
                return _res

            return self.to_json_safe(_res)

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose, raw_page_responses=raw_page_responses)

    # Technical Indicators
    def get_sma(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Simple Moving Average for an Index.

        :param symbol: The Index ticket symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return self._get_sma(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    def get_ema(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Exponential Moving Average for an Index.

        :param symbol: The Index ticket symbol.
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return self._get_ema(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    def get_rsi(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 14,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Relative Strength Index for an Index.

        :param symbol: The Index ticket symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return self._get_rsi(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    def get_macd(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        long_window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        short_window_size: int = 50,
        signal_window_size: int = 50,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Moving Average Convergence/Divergence for an Index.

        :param symbol: The Index ticker symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return self._get_macd(
            symbol,
            timestamp,
            timespan,
            adjusted,
            long_window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            short_window_size,
            signal_window_size,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )


# ========================================================= #


class AsyncIndexClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the Index REST endpoints. Note that you should always import names from top level.
    e.g.: ``from polygon import IndexClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    async def get_previous_close(self, symbol: str, raw_response: bool = False):
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified index.
        `Official Docs <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__prev>`__

        :param symbol: The ticker symbol of index (with or without the prefix `I:`)
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        _path = f"/v2/aggs/ticker/{ensure_prefix(symbol)}/prev"
        _data = {}

        _res = await self._get_response(_path, params=_data)
        if raw_response:
            return _res

        return self.to_json_safe(_res)

    async def get_daily_open_close(self, symbol: str, date, raw_response: bool = False):
        """
        Get the open, close and afterhours values of an index symbol on a certain date.
        `Official Docs <https://polygon.io/docs/indices/get_v1_open-close__indicesticker___date>`__

        :param symbol: The ticker symbol of index (with or without the prefix `I:`)
        :param date: The date/day for which to retrieve the data. Could be ``datetime`` or ``date`` or string
                     ``YYYY-MM-DD``
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        date = self.normalize_datetime(date, output_type="str")
        _path = f"/v1/open-close/{ensure_prefix(symbol)}/{date}"
        _data = {}

        _res = await self._get_response(_path, params=_data)
        if raw_response:
            return _res

        return self.to_json_safe(_res)

    async def get_aggregate_bars(
        self,
        symbol: str,
        from_date,
        to_date,
        sort="asc",
        limit: int = 5000,
        multiplier: int = 1,
        timespan="day",
        adjusted: bool = False,
        full_range: bool = False,
        run_parallel: bool = True,
        max_concurrent_workers: int = cpu_count() * 5,
        warnings: bool = True,
        info: bool = True,
        high_volatility: bool = False,
        raw_response: bool = False,
    ):
        """
        Get aggregate bars for an index over a given date range in custom time window sizes.
        For example, if ``timespan = ‘minute’`` and ``multiplier = ‘5’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the Index.
        :param from_date: The start of the aggregate time window. Could be ``datetime`` or ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime`` or ``date`` or string ``YYYY-MM-DD``
        :param sort: Sort the results by timestamp. See :class:`polygon.enums.SortOrder` for choices. ``asc`` default.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and
                      Default 5000.
        :param multiplier: The size of the timespan multiplier. Must be a positive whole number.
        :param timespan: The size of the time window. See :class:`polygon.enums.Timespan` for choices. defaults to
                         ``day``
        :param adjusted: NOT applicable on Indices. Changing this will have NO IMPACT.
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
        :param info: Set to False to disable printing mild warnings / informational messages if any when fetching the
                     aggs. E.g. if there was no data in a response but the response had an OK status
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (e.g. SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. Will be ignored if ``full_range=True``
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If ``full_range=True``, will return a single list with all the candles in it.
        """

        if not full_range:
            from_date = self.normalize_datetime(from_date, output_type="nts")

            to_date = self.normalize_datetime(to_date, output_type="nts", _dir="end")

            if timespan == "min":
                timespan = "minute"

            timespan, sort = self._change_enum(timespan, str), self._change_enum(sort, str)

            _path = f"/v2/aggs/ticker/{ensure_prefix(symbol)}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

            _data = {"sort": sort, "limit": limit}

            _res = await self._get_response(_path, params=_data)

            if raw_response:
                return _res

            return self.to_json_safe(_res)

        # The full range agg begins
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return await self.get_full_range_aggregates(
                self.get_aggregate_bars,
                symbol,
                time_chunks,
                run_parallel,
                max_concurrent_workers,
                warnings,
                info=info,
                adjusted=adjusted,
                multiplier=multiplier,
                sort=sort,
                limit=limit,
                timespan=timespan,
            )

        # Sequential Run
        time_chunks = [from_date, to_date]
        return await self.get_full_range_aggregates(
            self.get_aggregate_bars,
            symbol,
            time_chunks,
            run_parallel,
            max_concurrent_workers,
            warnings,
            info=info,
            adjusted=adjusted,
            multiplier=multiplier,
            sort=sort,
            limit=limit,
            timespan=timespan,
        )

    async def get_full_range_aggregate_bars(
        self,
        symbol: str,
        from_date,
        to_date,
        multiplier: int = 1,
        timespan="min",
        sort="asc",
        adjusted: bool = False,
        run_parallel: bool = True,
        max_concurrent_workers: int = cpu_count() * 5,
        warnings: bool = True,
        info: bool = True,
        high_volatility: bool = False,
    ):
        """
        Get BULK full range aggregate bars (OCHLV candles) for an Index.
        For example, if ``timespan=‘minute’`` and ``multiplier=‘1’`` then 5-minute bars will be returned.
        `Official Docs
        <https://polygon.io/docs/indices/get_v2_aggs_ticker__indicesticker__range__multiplier___timespan___from___to>`__

        :param symbol: The ticker symbol of the Index. e.g.: ``I:NDX``. You can specify with or without prefix
                       ``I:``
        :param from_date: The start of the aggregate time window. Could be ``datetime``, ``date`` or string
                          ``YYYY-MM-DD``
        :param to_date: The end of the aggregate time window. Could be ``datetime``, ``date`` or string ``YYYY-MM-DD``
        :param multiplier: The size of the timespan multiplier
        :param timespan: The size of the time window. Defaults to minute candles. see :class:`polygon.enums.Timespan`
                         for choices
        :param sort: Order of sorting the results. See :class:`polygon.enums.SortOrder` for available choices.
                     Defaults to ``asc`` (oldest at the top)
        :param adjusted: NOT applicable on Indices. Changing this will have NO IMPACT.
        :param run_parallel: Only considered if ``full_range=True``. If set to true (default True), it will run an
                             internal ThreadPool to get the responses. This is fine to do if you are not running your
                             own ThreadPool. If you have many tickers to get aggs for, it's better to either use the
                             async version of it OR set this to False and spawn threads for each ticker yourself.
        :param max_concurrent_workers: Only considered if ``run_parallel=True``. Defaults to ``your cpu cores * 5``.
                                       controls how many worker threads to use in internal ThreadPool
        :param warnings: Set to False to disable printing warnings if any when fetching the aggs. Defaults to True.
        :param info: Set to False to disable printing mild warnings / informational messages if any when fetching the
                     aggs. E.g. if there was no data in a response but the response had an OK status
        :param high_volatility: Specifies whether the symbol/security in question is highly volatile which just means
                                having a very high number of trades or being traded for a high duration (e.g. SPY,
                                Bitcoin) If set to True, the lib will use a smaller chunk of time to ensure we don't
                                miss any data due to 50k candle limit. Defaults to False.
        :return: a single list with all the candles.
        """
        if run_parallel:  # Parallel Run
            time_chunks = self.split_date_range(from_date, to_date, timespan, high_volatility=high_volatility)
            return await self.get_full_range_aggregates(
                self.get_aggregate_bars,
                symbol,
                time_chunks,
                run_parallel,
                max_concurrent_workers,
                warnings,
                info=info,
                adjusted=adjusted,
                multiplier=multiplier,
                sort=sort,
                limit=50_000,
                timespan=timespan,
            )

        # Sequential Run
        time_chunks = [from_date, to_date]
        return await self.get_full_range_aggregates(
            self.get_aggregate_bars,
            symbol,
            time_chunks,
            run_parallel,
            max_concurrent_workers,
            warnings,
            info=info,
            adjusted=adjusted,
            multiplier=multiplier,
            sort=sort,
            limit=50_000,
            timespan=timespan,
        )

    async def get_snapshot(
        self,
        symbols: list = None,
        order="desc",
        limit: int = 5000,
        sort="ticker",
        ticker_lt: str = None,
        ticker_lte: str = None,
        ticker_gt: str = None,
        ticker_gte: str = None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get a Snapshot of indices data for said tickers
        `Official Docs <https://polygon.io/docs/indices/get_v3_snapshot_indices>`__

        :param symbols: list of Index tickers, up to a maximum of 250. Defaults to ALL tickers
        :param ticker_lt: Return results where this field is less than the value given
        :param ticker_lte: Return results where this field is less than or equal to the value given
        :param ticker_gt: Return results where this field is greater than the value given
        :param ticker_gte: Return results where this field is greater than or equal to the value given
        :param sort: Sort field key used for ordering. 'ticker' default. see
                     :class:`polygon.enums.IndexSnapshotSortKey` for choices.
        :param order: The order to sort the results on. Default is asc. See :class:`polygon.enums.SortOrder` for
                      available choices.
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
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
        :param raw_response: whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = f"/v3/snapshot/indices"

        if symbols is not None:
            tickers = ",".join([ensure_prefix(x) for x in symbols])
        else:
            tickers = None

        _data = {
            "ticker.any_of": tickers,
            "ticker.lt": ticker_lt,
            "ticker.lte": ticker_lte,
            "ticker.gt": ticker_gt,
            "ticker.gte": ticker_gte,
            "limit": limit,
            "sort": self._change_enum(sort, str),
            "order": self._change_enum(order, str),
        }

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginate!!
            if raw_response:
                return _res

            return self.to_json_safe(_res)

        return await self._paginate(
            _res, merge_all_pages, max_pages, verbose=verbose, raw_page_responses=raw_page_responses
        )

    # Technical Indicators
    async def get_sma(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Simple Moving Average for an Index.

        :param symbol: The Index ticket symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return await self._get_sma(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    async def get_ema(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Exponential Moving Average for an Index.

        :param symbol: The Index ticket symbol.
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return await self._get_ema(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    async def get_rsi(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        window_size: int = 14,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Relative Strength Index for an Index.

        :param symbol: The Index ticket symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return await self._get_rsi(
            symbol,
            timestamp,
            timespan,
            adjusted,
            window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )

    async def get_macd(
        self,
        symbol: str,
        timestamp=None,
        timespan="day",
        adjusted: bool = True,
        long_window_size: int = 50,
        series_type="close",
        include_underlying: bool = False,
        order="desc",
        limit: int = 5000,
        timestamp_lt=None,
        timestamp_lte=None,
        timestamp_gt=None,
        timestamp_gte=None,
        short_window_size: int = 50,
        signal_window_size: int = 50,
        all_pages: bool = False,
        max_pages: int = None,
        merge_all_pages: bool = True,
        verbose: bool = False,
        raw_page_responses: bool = False,
        raw_response: bool = False,
    ):
        """
        Get the Moving Average Convergence/Divergence for an Index.

        :param symbol: The Index ticker symbol
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
        :param raw_response: Whether to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: The response object
        """
        symbol = ensure_prefix(symbol)

        return await self._get_macd(
            symbol,
            timestamp,
            timespan,
            adjusted,
            long_window_size,
            series_type,
            include_underlying,
            order,
            limit,
            timestamp_lt,
            timestamp_lte,
            timestamp_gt,
            timestamp_gte,
            short_window_size,
            signal_window_size,
            all_pages,
            max_pages,
            merge_all_pages,
            verbose,
            raw_page_responses,
            raw_response,
        )


# ========================================================= #


def ensure_prefix(sym: str):
    if sym.upper().startswith("I:"):
        return sym.upper()

    return f"I:{sym.upper()}"
