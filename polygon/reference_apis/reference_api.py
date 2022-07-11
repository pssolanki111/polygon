# ========================================================= #
from .. import base_client
import os
from collections import OrderedDict
import asyncio

# ========================================================= #


def ReferenceClient(api_key: str, use_async: bool = False, connect_timeout: int = 10, read_timeout: int = 10,
                    pool_timeout: int = 10, max_connections: int = None, max_keepalive: int = None,
                    write_timeout: int = 10):
    """
    Initiates a Client to be used to access all REST References endpoints.

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
        return SyncReferenceClient(api_key, connect_timeout, read_timeout)

    return AsyncReferenceClient(api_key, connect_timeout, read_timeout, pool_timeout, max_connections,
                                max_keepalive, write_timeout)


# ========================================================= #


class SyncReferenceClient(base_client.BaseClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the References REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ReferenceClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout)

    # Endpoints
    def get_tickers(self, symbol: str = '', ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None,
                    symbol_type='', market='', exchange: str = '', cusip: str = None, cik: str = '',
                    date=None, search: str = None,
                    active: bool = True, sort='ticker', order='asc', limit: int = 1000, all_pages: bool = False,
                    max_pages: int = None, merge_all_pages: bool = True, verbose: bool = False,
                    raw_page_responses: bool = False, raw_response: bool = False):
        """
        Query all ticker symbols which are supported by Polygon.io. This API currently includes Stocks/Equities, Crypto,
        and Forex.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers>`__

        :param symbol: Specify a ticker symbol. Defaults to empty string which queries all tickers.
        :param ticker_lt: Return results where this field is less than the value given
        :param ticker_lte: Return results where this field is less than or equal to the value given
        :param ticker_gt: Return results where this field is greater than the value given
        :param ticker_gte: Return results where this field is greater than or equal to the value given
        :param symbol_type: Specify the type of the tickers. See :class:`polygon.enums.TickerType` for common choices.
                            Find all supported types via the `Ticker Types API
                            <https://polygon.io/docs/stocks/get_v3_reference_tickers_types>`__
                            Defaults to empty string which queries all types.
        :param market: Filter by market type. By default all markets are included. See
                       :class:`polygon.enums.TickerMarketType` for available choices.
        :param exchange: Specify the primary exchange of the asset in the ISO code format. Find more information about
                         the ISO codes at the `ISO org website <https://www.iso20022.org/market-identifier-codes>`__.
                         Defaults to empty string which queries all exchanges.
        :param cusip: Specify the ``CUSIP`` code of the asset you want to search for. Find more information about CUSIP
                      codes on `their website <https://www.cusip.com/identifiers.html#/CUSIP>`__
                      Defaults to empty string which queries all CUSIPs
        :param cik: Specify the ``CIK`` of the asset you want to search for. Find more information about CIK codes at
                    `their website <https://www.sec.gov/edgar/searchedgar/cik.htm>`__
                    Defaults to empty string which queries all CIKs.
        :param date: Specify a point in time to retrieve tickers available on that date. Defaults to the most recent
                     available date. Could be ``datetime``, ``date`` or a string ``YYYY-MM-DD``
        :param search: Search for terms within the ticker and/or company name. for eg ``MS`` will match matching symbols
        :param active: Specify if the tickers returned should be actively traded on the queried date. Default is True
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present,
                     sort is ignored and results are ordered by relevance. See :class:`polygon.enums.TickerSortType`
                     for available choices.
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
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """

        date = self.normalize_datetime(date, output_type='str')

        symbol_type, market = self._change_enum(symbol_type, str), self._change_enum(market, str)
        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = '/v3/reference/tickers'

        _data = {'ticker': symbol, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'type': symbol_type, 'market': market, 'exchange': exchange,
                 'cusip': cusip, 'cik': cik, 'date': date, 'search': search, 'active': active, 'sort': sort,
                 'order': order, 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_ticker_types(self, asset_class=None, locale=None, raw_response: bool = False):
        """
        Get a mapping of ticker types to their descriptive names.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers_types>`__

        :param asset_class: Filter by asset class. see :class:`polygon.enums.AssetClass` for choices
        :param locale: Filter by locale. See :class:`polygon.enums.Locale` for choices
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        asset_class, locale = self._change_enum(asset_class, str), self._change_enum(locale, str)

        _path = '/v3/reference/tickers/types'

        _data = {'asset_class': asset_class,
                 'locale': locale}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_ticker_details(self, symbol: str, date=None, raw_response: bool = False):
        """
        Get a single ticker supported by Polygon.io. This response will have detailed information about the ticker and
        the company behind it.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker>`__

        :param symbol: The ticker symbol of the asset.
        :param date: Specify a point in time to get information about the ticker available on that date. When retrieving
                     information from SEC filings, we compare this date with the period of report date on the SEC
                     filing. Defaults to the most recent available date.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v3/reference/tickers/{symbol.upper()}'

        _data = {'date': date}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()
    
    def get_bulk_ticker_details(self, symbol: str, from_date=None, to_date=None, custom_dates: list = None,
                                run_parallel: bool = True, warnings: bool = True, sort='asc',
                                max_concurrent_workers: int = os.cpu_count() * 5) -> OrderedDict:
        """
        Get ticker details for a symbol for specified date range and/or dates.
        Each response will have detailed information about the ticker and the company behind it (on THAT particular 
        date) `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker>`__
        
        :param symbol: The ticker symbol to get data for
        :param from_date: The start date of the date range. Must be specified if custom_dates is not supplied
        :param to_date: The end date of the date range. Must be specified if custom_dates is not supplied
        :param custom_dates: A list of dates, for which to get data for. You can specify this WITH a range. Each date 
                             can be a ``date``, ``datetime`` object or a string ``YYYY-MM-DD``
        :param run_parallel: If true (the default), it will use an internal ``ThreadPool`` to get the responses in
                             parallel. **Note That** since python has the GIL restrictions, it would mean that if you
                             have a ThreadPool of your own, only one ThreadPool will be running at a time and the
                             other pool will wait. set to False to get all responses in sequence (will take time)
        :param warnings: Defaults to True which prints warnings. Set to False to disable warnings.
        :param sort: The order of sorting the final results. Defaults to ascending order of dates. See 
                     :class:`polygon.enums.SortOrder` for choices
        :param max_concurrent_workers: This is only used if run_parallel is set to true. Controls how many worker
                                       threads are spawned in the internal thread pool. Defaults to ``your cpu core
                                       count * 5``
        :return: An OrderedDict where keys are dates, and values are corresponding ticker details.
        """
        
        if custom_dates is None:
            if from_date is None or to_date is None:
                raise ValueError('You must supply either custom_dates or (from_date and to_date)')
            else:
                all_dates = self.get_dates_between(from_date, to_date)
        else:
            custom_dates = [self.normalize_datetime(dt, output_type='date') for dt in custom_dates]
            all_dates = sorted(list(set(custom_dates + self.get_dates_between(from_date, to_date))))
            
        # Start off with the requests
        futures, final_results, sort_order = OrderedDict(), OrderedDict(), self._change_enum(sort, str)
        
        if run_parallel:  # parallel run
            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=max_concurrent_workers) as pool:
                for dt in all_dates:
                    futures[dt] = pool.submit(self.get_ticker_details, symbol, dt)

            for future in futures:
                try:
                    data = futures[future].result()
                except:
                    if warnings:
                        print(f'No data for {symbol} on {future}. response: {future.result()}')
                    data = None

                final_results[future] = data

            return final_results if sort_order == 'asc' else OrderedDict(reversed(list(final_results.items())))
        
        # Sequential Run
        for dt in all_dates:
            try:
                data = self.get_ticker_details(symbol, dt)
                final_results[dt] = data
            except:
                final_results[dt] = None
            
        return final_results if sort_order == 'asc' else OrderedDict(reversed(list(final_results.items())))

    def get_option_contract(self, ticker: str, as_of_date=None, raw_response: bool = False):
        """
        get Info about an option contract
        `Official Docs <https://polygon.io/docs/options/get_v3_reference_options_contracts__options_ticker>`__

        :param ticker: An option ticker in standard format. The lib provides `easy functions
                       <https://polygon.readthedocs.io/en/latest/Options.html#creating-option-symbols>`__
                       to build and work with option symbols
        :param as_of_date: Specify a point in time for the contract. You can pass a ``datetime`` or ``date`` object or
                           a string in format ``YYYY-MM-DD``. Defaults to today's date
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        as_of_date = self.normalize_datetime(as_of_date, output_type='str')

        _path = f'/v3/reference/options/contracts/{ensure_prefix(ticker)}'

        _data = {'as_of': as_of_date}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_option_contracts(self, underlying_ticker: str = None, ticker: str = None, contract_type=None,
                             expiration_date=None, expiration_date_lt=None, expiration_date_lte=None,
                             expiration_date_gt=None, expiration_date_gte=None, order='asc', sort='expiration_date',
                             limit=1000, all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                             verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        List currently active options contracts
        `Official Docs <https://polygon.io/docs/options/get_v3_reference_options_contracts>`__

        :param underlying_ticker: Query for contracts relating to an underlying stock ticker.
        :param ticker: Query for a contract by option ticker.
        :param contract_type: Query by the type of contract. see :class:`polygon.enums.OptionsContractType` for choices
        :param expiration_date: Query by contract expiration date. either ``datetime``, ``date`` or string
                                ``YYYY-MM-DD``
        :param expiration_date_lt: expiration date less than given value
        :param expiration_date_lte: expiration date less than equal to given value
        :param expiration_date_gt: expiration_date greater than given value
        :param expiration_date_gte: expiration_date greater than equal to given value
        :param order: Order of results. See :class:`polygon.enums.SortOrder` for choices.
        :param sort: Sort field for ordering. See :class:`polygon.enums.OptionsContractsSortType` for choices.
                     defaults to expiration_date
        :param limit: Limit the size of the response, default is 1000.
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
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """
        expiration_date = self.normalize_datetime(expiration_date, output_type='str')

        expiration_date_lt = self.normalize_datetime(expiration_date_lt, output_type='str')

        expiration_date_lte = self.normalize_datetime(expiration_date_lte, output_type='str')

        expiration_date_gt = self.normalize_datetime(expiration_date_gt, output_type='str')

        expiration_date_gte = self.normalize_datetime(expiration_date_gte, output_type='str')

        contract_type = self._change_enum(contract_type, str)
        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = f'/v3/reference/options/contracts'

        _data = {'ticker': ticker, 'underlying_ticker': underlying_ticker, 'contract_type': contract_type,
                 'expiration_date': expiration_date, 'expiration_date.lt': expiration_date_lt,
                 'expiration_date.lte': expiration_date_lte, 'expiration_date.gt': expiration_date_gt,
                 'expiration_date.gte': expiration_date_gte, 'order': order, 'sort': sort, 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_ticker_news(self, symbol: str = None, limit: int = 1000, order='desc', sort='published_utc',
                        ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None, published_utc=None,
                        published_utc_lt=None, published_utc_lte=None, published_utc_gt=None, published_utc_gte=None,
                        all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                        verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get the most recent news articles relating to a stock ticker symbol, including a summary of the article and a
        link to the original source.
        `Official Docs <https://polygon.io/docs/options/get_v2_reference_news>`__

        :param symbol: To get news mentioning the name given. Defaults to empty string which doesn't filter tickers
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param order: Order the results. See :class:`polygon.enums.SortOrder` for choices.
        :param sort: The field key to sort. See :class:`polygon.enums.TickerNewsSort` for choices.
        :param ticker_lt: Return results where this field is less than the value.
        :param ticker_lte: Return results where this field is less than or equal to the value.
        :param ticker_gt: Return results where this field is greater than the value
        :param ticker_gte: Return results where this field is greater than or equal to the value.
        :param published_utc: A date string ``YYYY-MM-DD`` or ``datetime`` for published date time filters.
        :param published_utc_lt: Return results where this field is less than the value given
        :param published_utc_lte: Return results where this field is less than or equal to the value given
        :param published_utc_gt: Return results where this field is greater than the value given
        :param published_utc_gte: Return results where this field is greater than or equal to the value given
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

        published_utc = self.normalize_datetime(published_utc, output_type='str')

        published_utc_lt = self.normalize_datetime(published_utc_lt)

        published_utc_lte = self.normalize_datetime(published_utc_lte)

        published_utc_gt = self.normalize_datetime(published_utc_gt)

        published_utc_gte = self.normalize_datetime(published_utc_gte)

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = '/v2/reference/news'

        _data = {'limit': limit, 'order': order, 'sort': sort, 'ticker': symbol, 'ticker.lt': ticker_lt,
                 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt, 'ticker.gte': ticker_gte,
                 'published_utc': published_utc, 'published_utc.lt': published_utc_lt,
                 'published_utc.lte': published_utc_lte, 'published_utc.gt': published_utc_gt,
                 'published_utc.gte': published_utc_gte}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_stock_dividends(self, ticker: str = None, ex_dividend_date=None, record_date=None,
                            declaration_date=None, pay_date=None, frequency: int = None, limit: int = 1000,
                            cash_amount=None, dividend_type=None, sort: str = 'pay_date', order: str = 'asc',
                            ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None,
                            ex_dividend_date_lt=None, ex_dividend_date_lte=None, ex_dividend_date_gt=None,
                            ex_dividend_date_gte=None, record_date_lt=None, record_date_lte=None,
                            record_date_gt=None, record_date_gte=None, declaration_date_lt=None,
                            declaration_date_lte=None, declaration_date_gt=None, declaration_date_gte=None,
                            pay_date_lt=None, pay_date_lte=None, pay_date_gt=None, pay_date_gte=None,
                            cash_amount_lt=None, cash_amount_lte=None, cash_amount_gt=None, cash_amount_gte=None,
                            all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                            verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get a list of historical cash dividends, including the ticker symbol, declaration date, ex-dividend date,
        record date, pay date, frequency, and amount.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_dividends>`__

        :param ticker: Return the dividends that contain this ticker.
        :param ex_dividend_date: Query by ex-dividend date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param record_date: Query by record date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param declaration_date: Query by declaration date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param pay_date: Query by pay date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param frequency: Query by the number of times per year the dividend is paid out. No default value applied.
                          see :class:`polygon.enums.PayoutFrequency` for choices
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param cash_amount: Query by the cash amount of the dividend.
        :param dividend_type: Query by the type of dividend. See :class:`polygon.enums.DividendType` for choices
        :param sort: sort key used for ordering. See :class:`polygon.enums.DividendSort` for choices.
        :param order: orders of results. defaults to asc. see :class:`polygon.enums.SortOrder` for choices
        :param ticker_lt: filter where ticker is less than given value (alphabetically)
        :param ticker_lte: filter where ticker is less than or equal to given value (alphabetically)
        :param ticker_gt: filter where ticker is greater than given value (alphabetically)
        :param ticker_gte: filter where ticker is greater than or equal to given value (alphabetically)
        :param ex_dividend_date_lt: filter where ex-div date is less than given date
        :param ex_dividend_date_lte: filter where ex-div date is less than or equal to given date
        :param ex_dividend_date_gt: filter where ex-div date is greater than given date
        :param ex_dividend_date_gte: filter where ex-div date is greater than or equal to given date
        :param record_date_lt: filter where record date is less than given date
        :param record_date_lte: filter where record date is less than or equal to given date
        :param record_date_gt: filter where record date is greater than given date
        :param record_date_gte: filter where record date is greater than or equal to given date
        :param declaration_date_lt: filter where declaration date is less than given date
        :param declaration_date_lte: filter where declaration date is less than or equal to given date
        :param declaration_date_gt: filter where declaration date is greater than given date
        :param declaration_date_gte: filter where declaration date is greater than or equal to given date
        :param pay_date_lt: filter where pay date is less than given date
        :param pay_date_lte: filter where pay date is less than or equal to given date
        :param pay_date_gt: filter where pay date is greater than given date
        :param pay_date_gte: filter where pay date is greater than or equal to given date
        :param cash_amount_lt: filter where cash amt is less than given value
        :param cash_amount_lte: filter where cash amt is less than or equal to given value
        :param cash_amount_gt: filter where cash amt is greater than given value
        :param cash_amount_gte: filter where cash amt is greater than or equal to given value
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

        ex_dividend_date = self.normalize_datetime(ex_dividend_date, output_type='str')

        record_date = self.normalize_datetime(record_date, output_type='str')

        declaration_date = self.normalize_datetime(declaration_date, output_type='str')

        pay_date = self.normalize_datetime(pay_date, output_type='str')

        ex_dividend_date_lt = self.normalize_datetime(ex_dividend_date_lt, output_type='str')

        ex_dividend_date_lte = self.normalize_datetime(ex_dividend_date_lte, output_type='str')

        ex_dividend_date_gt = self.normalize_datetime(ex_dividend_date_gt, output_type='str')

        ex_dividend_date_gte = self.normalize_datetime(ex_dividend_date_gte, output_type='str')

        record_date_lt = self.normalize_datetime(record_date_lt, output_type='str')

        record_date_lte = self.normalize_datetime(record_date_lte, output_type='str')

        record_date_gt = self.normalize_datetime(record_date_gt, output_type='str')

        record_date_gte = self.normalize_datetime(record_date_gte, output_type='str')

        declaration_date_lt = self.normalize_datetime(declaration_date_lt, output_type='str')

        declaration_date_lte = self.normalize_datetime(declaration_date_lte, output_type='str')

        declaration_date_gt = self.normalize_datetime(declaration_date_gt, output_type='str')

        declaration_date_gte = self.normalize_datetime(declaration_date_gte, output_type='str')

        pay_date_lt = self.normalize_datetime(pay_date_lt, output_type='str')

        pay_date_lte = self.normalize_datetime(pay_date_lte, output_type='str')

        pay_date_gt = self.normalize_datetime(pay_date_gt, output_type='str')

        pay_date_gte = self.normalize_datetime(pay_date_gte, output_type='str')

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)
        frequency, dividend_type = self._change_enum(frequency, int), self._change_enum(dividend_type, str)

        _path = f'/v3/reference/dividends'

        _data = {'ticker': ticker, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'ex_dividend_date': ex_dividend_date,
                 'ex_dividend_date.lt': ex_dividend_date_lt, 'ex_dividend_date.lte': ex_dividend_date_lte,
                 'ex_dividend_date.gt': ex_dividend_date_gt, 'ex_dividend_date.gte': ex_dividend_date_gte,
                 'record_date': record_date, 'record_date.lt': record_date_lt, 'record_date.lte': record_date_lte,
                 'record_date.gt': record_date_gt, 'record_date.gte': record_date_gte,
                 'declaration_date': declaration_date, 'declaration_date.lt': declaration_date_lt,
                 'declaration_date.lte': declaration_date_lte, 'declaration_date.gt': declaration_date_gt,
                 'declaration_date.gte': declaration_date_gte, 'pay_date': pay_date, 'pay_date.lt': pay_date_lt,
                 'pay_date.lte': pay_date_lte, 'pay_date.gt': pay_date_gt, 'pay_date.gte': pay_date_gte,
                 'frequency': frequency, 'cash_amount': cash_amount, 'cash_amount.lt': cash_amount_lt,
                 'cash_amount.lte': cash_amount_lte, 'cash_amount.gt': cash_amount_gt,
                 'cash_amount.gte': cash_amount_gte, 'dividend_type': dividend_type, 'order': order, 'sort': sort,
                 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_stock_financials_vx(self, ticker: str = None, cik: str = None, company_name: str = None,
                                company_name_search: str = None, sic: str = None, filing_date=None,
                                filing_date_lt=None, filing_date_lte=None, filing_date_gt=None, filing_date_gte=None,
                                period_of_report_date=None, period_of_report_date_lt=None,
                                period_of_report_date_lte=None, period_of_report_date_gt=None,
                                period_of_report_date_gte=None, time_frame=None, include_sources: bool = False,
                                order='asc', limit: int = 50, sort='filing_date',
                                raw_response: bool = False):
        """
        Get historical financial data for a stock ticker. The financials data is extracted from XBRL from company SEC
        filings using `this methodology <http://xbrl.squarespace.com/understanding-sec-xbrl-financi/>`__
        `Official Docs <https://polygon.io/docs/stocks/get_vx_reference_financials>`__

        This API is experimental and will replace :meth:`get_stock_financials` in future.

        :param ticker: Filter query by company ticker.
        :param cik: filter the Query by ``central index key (CIK)`` Number
        :param company_name: filter the query by company name
        :param company_name_search: partial match text search for company names
        :param sic: Query by ``standard industrial classification (SIC)``
        :param filing_date: Query by the date when the filing with financials data was filed. ``datetime/date`` or
                            string ``YYYY-MM-DD``
        :param filing_date_lt: filter for filing date less than given value
        :param filing_date_lte: filter for filing date less than equal to given value
        :param filing_date_gt: filter for filing date greater than given value
        :param filing_date_gte: filter for filing date greater than equal to given value
        :param period_of_report_date: query by The period of report for the filing with financials data.
                                      ``datetime/date`` or string in format: ``YYY-MM-DD``.
        :param period_of_report_date_lt: filter for period of report date less than given value
        :param period_of_report_date_lte: filter for period of report date less than equal to given value
        :param period_of_report_date_gt: filter for period of report date greater than given value
        :param period_of_report_date_gte: filter for period of report date greater than equal to given value
        :param time_frame: Query by timeframe. Annual financials originate from 10-K filings, and quarterly financials
                           originate from 10-Q filings. Note: Most companies do not file quarterly reports for Q4 and
                           instead include those financials in their annual report, so some companies my not return
                           quarterly financials for Q4. See :class:`polygon.enums.StockFinancialsTimeframe` for choices.
        :param include_sources: Whether or not to include the xpath and formula attributes for each financial data
                                point. See the xpath and formula response attributes for more info. ``False`` by default
        :param order: Order results based on the sort field. 'asc' by default. See :class:`polygon.enums.SortOrder`
                      for choices.
        :param limit: number of max results to obtain. defaults to 50.
        :param sort: Sort field key used for ordering. 'filing_date' default. see
                     :class:`polygon.enums.StockFinancialsSortKey` for choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        filing_date = self.normalize_datetime(filing_date, output_type='str')

        period_of_report_date = self.normalize_datetime(period_of_report_date, output_type='str')

        filing_date_lt = self.normalize_datetime(filing_date_lt, output_type='str')

        filing_date_lte = self.normalize_datetime(filing_date_lte, output_type='str')

        filing_date_gt = self.normalize_datetime(filing_date_gt, output_type='str')

        filing_date_gte = self.normalize_datetime(filing_date_gte, output_type='str')

        period_of_report_date_lt = self.normalize_datetime(period_of_report_date_lt, output_type='str')

        period_of_report_date_lte = self.normalize_datetime(period_of_report_date_lte, output_type='str')

        period_of_report_date_gt = self.normalize_datetime(period_of_report_date_gt, output_type='str')

        period_of_report_date_gte = self.normalize_datetime(period_of_report_date_gte, output_type='str')

        time_frame = self._change_enum(time_frame)
        order, sort = self._change_enum(order), self._change_enum(sort)

        _path = f'/vX/reference/financials'

        _data = {'ticker': ticker, 'cik': cik, 'company_name': company_name,
                 'company_name_search': company_name_search, 'sic': sic, 'filing_date': filing_date,
                 'filing_date.lt': filing_date_lt, 'filing_date.lte': filing_date_lte,
                 'filing_date.gt': filing_date_gt, 'filing_date.gte': filing_date_gte,
                 'period_of_report_date': period_of_report_date, 'period_of_report_date.lt': period_of_report_date_lt,
                 'period_of_report_date.lte': period_of_report_date_lte,
                 'period_of_report_date.gt': period_of_report_date_gt,
                 'period_of_report_date.gte': period_of_report_date_gte, 'timeframe': time_frame, 'order': order,
                 'include_sources': 'true' if include_sources else 'false', 'limit': limit, 'sort': sort}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_stock_splits(self, ticker: str = None, execution_date=None, reverse_split: bool = None, order: str = 'asc',
                         sort: str = 'execution_date', limit: int = 1000, ticker_lt=None, ticker_lte=None,
                         ticker_gt=None, ticker_gte=None, execution_date_lt=None, execution_date_lte=None,
                         execution_date_gt=None, execution_date_gte=None, all_pages: bool = False,
                         max_pages: int = None, merge_all_pages: bool = True, verbose: bool = False,
                         raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get a list of historical stock splits, including the ticker symbol, the execution date, and the factors of
        the split ratio.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_splits>`__

        :param ticker: Return the stock splits that contain this ticker. defaults to no ticker filter returning all.
        :param execution_date: query by execution date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param reverse_split: Query for reverse stock splits. A split ratio where split_from is greater than split_to
               represents a reverse split. By default this filter is not used.
        :param order: Order results based on the sort field. defaults to ascending. See
               :class:`polygon.enums.SortOrder` for choices
        :param sort: Sort field used for ordering. Defaults to 'execution_date'. See
               :class:`polygon.enums.SplitsSortKey` for choices.
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param ticker_lt: filter where ticker name is less than given value (alphabetically)
        :param ticker_lte: filter where ticker name is less than or equal to given value (alphabetically)
        :param ticker_gt: filter where ticker name is greater than given value (alphabetically)
        :param ticker_gte: filter where ticker name is greater than or equal to given value (alphabetically)
        :param execution_date_lt: filter where execution date is less than given value
        :param execution_date_lte: filter where execution date is less than or equal to given value
        :param execution_date_gt: filter where execution date is greater than given value
        :param execution_date_gte: filter where execution date is greater than or equal to given value
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

        execution_date = self.normalize_datetime(execution_date, output_type='str')

        execution_date_lt = self.normalize_datetime(execution_date_lt, output_type='str')

        execution_date_lte = self.normalize_datetime(execution_date_lte, output_type='str')

        execution_date_gt = self.normalize_datetime(execution_date_gt, output_type='str')

        execution_date_gte = self.normalize_datetime(execution_date_gte, output_type='str')

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = f'/v3/reference/splits'

        _data = {'ticker': ticker, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'execution_date': execution_date, 'execution_date.lt': execution_date_lt,
                 'execution_date.lte': execution_date_lte, 'execution_date.gt': execution_date_gt,
                 'execution_date.gte': execution_date_gte, 'reverse_split': reverse_split, 'order': order,
                 'sort': sort, 'limit': limit}

        _res = self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                              raw_page_responses=raw_page_responses)

    def get_market_holidays(self, raw_response: bool = False):
        """
        Get upcoming market holidays and their open/close times.
        `Official Docs <https://polygon.io/docs/stocks/get_v1_marketstatus_upcoming>`__

        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = '/v1/marketstatus/upcoming'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_market_status(self, raw_response: bool = False):
        """
        Get the current trading status of the exchanges and overall financial markets.
        `Official Docs <https://polygon.io/docs/stocks/get_v1_marketstatus_now>`__

        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = '/v1/marketstatus/now'

        _res = self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    def get_conditions(self, asset_class=None, data_type=None, condition_id=None, sip=None, order=None,
                       limit: int = 50, sort='name', raw_response: bool = False):
        """
        List all conditions that Polygon.io uses.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_conditions>`__

        :param asset_class: Filter for conditions within a given asset class. See :class:`polygon.enums.AssetClass`
                            for choices. Defaults to all assets.
        :param data_type: Filter by data type. See :class:`polygon.enums.ConditionsDataType` for choices. defaults to
                          all.
        :param condition_id: Filter for conditions with a given ID
        :param sip: Filter by SIP. If the condition contains a mapping for that SIP, the condition will be returned.
        :param order: Order results. See :class:`polygon.enums.SortOrder` for choices.
        :param limit: limit the number of results. defaults to 50.
        :param sort: Sort field used for ordering. Defaults to 'name'. See :class:`polygon.enums.ConditionsSortKey`
                     for choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        asset_class, data_type = self._change_enum(asset_class), self._change_enum(data_type)
        order, sort = self._change_enum(order), self._change_enum(sort)

        _path = f'/v3/reference/conditions'

        _data = {'asset_class': asset_class, 'data_type': data_type, 'id': condition_id, 'sip': sip, 'order': order,
                 'limit': limit, 'sort': sort}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    def get_exchanges(self, asset_class=None, locale=None, raw_response: bool = False):
        """
        List all exchanges that Polygon.io knows about.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_exchanges>`__

        :param asset_class: filter by asset class. See :class:`polygon.enums.AssetClass` for choices.
        :param locale: Filter by locale name. See :class:`polygon.enums.Locale`
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        asset_class, locale = self._change_enum(asset_class), self._change_enum(locale)

        _path = f'/v3/reference/exchanges'

        _data = {'asset_class': asset_class, 'locale': locale}

        _res = self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #

class AsyncReferenceClient(base_client.BaseAsyncClient):
    """
    These docs are not meant for general users. These are library API references. The actual docs will be
    available on the index page when they are prepared.

    This class implements all the References REST endpoints. Note that you should always import names from top level.
    eg: ``from polygon import ReferenceClient`` or ``import polygon`` (which allows you to access all names easily)
    """

    def __init__(self, api_key: str, connect_timeout: int = 10, read_timeout: int = 10, pool_timeout: int = 10,
                 max_connections: int = None, max_keepalive: int = None, write_timeout: int = 10):
        super().__init__(api_key, connect_timeout, read_timeout, pool_timeout, max_connections, max_keepalive,
                         write_timeout)

    # Endpoints
    async def get_tickers(self, symbol: str = '', ticker_lt=None, ticker_lte=None, ticker_gt=None,
                          ticker_gte=None, symbol_type='', market='', exchange: str = '',
                          cusip: str = None, cik: str = '', date=None, search: str = None, active: bool = True,
                          sort='ticker', order: str = 'asc', limit: int = 1000, all_pages: bool = False,
                          max_pages: int = None, merge_all_pages: bool = True, verbose: bool = False,
                          raw_page_responses: bool = False, raw_response: bool = False):
        """
        Query all ticker symbols which are supported by Polygon.io. This API currently includes Stocks/Equities, Crypto,
        and Forex.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers>`__

        :param symbol: Specify a ticker symbol. Defaults to empty string which queries all tickers.
        :param ticker_lt: Return results where this field is less than the value given
        :param ticker_lte: Return results where this field is less than or equal to the value given
        :param ticker_gt: Return results where this field is greater than the value given
        :param ticker_gte: Return results where this field is greater than or equal to the value given
        :param symbol_type: Specify the type of the tickers. See :class:`polygon.enums.TickerType` for common choices.
                            Find all supported types via the `Ticker Types API
                            <https://polygon.io/docs/get_v2_reference_types_anchor>`__
                            Defaults to empty string which queries all types.
        :param market: Filter by market type. By default all markets are included. See
                       :class:`polygon.enums.TickerMarketType` for available choices.
        :param exchange: Specify the primary exchange of the asset in the ISO code format. Find more information about
                         the ISO codes at the `ISO org website <https://www.iso20022.org/market-identifier-codes>`__.
                         Defaults to empty string which queries all exchanges.
        :param cusip: Specify the ``CUSIP`` code of the asset you want to search for. Find more information about CUSIP
                      codes on `their website <https://www.cusip.com/identifiers.html#/CUSIP>`__
                      Defaults to empty string which queries all CUSIPs
        :param cik: Specify the ``CIK`` of the asset you want to search for. Find more information about CIK codes at
                    `their website <https://www.sec.gov/edgar/searchedgar/cik.htm>`__
                    Defaults to empty string which queries all CIKs.
        :param date: Specify a point in time to retrieve tickers available on that date. Defaults to the most recent
                     available date. Could be ``datetime``, ``date`` or a string ``YYYY-MM-DD``
        :param search: Search for terms within the ticker and/or company name. for eg ``MS`` will match matching symbols
        :param active: Specify if the tickers returned should be actively traded on the queried date. Default is True
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present,
                     sort is ignored and results are ordered by relevance. See :class:`polygon.enums.TickerSortType`
                     for available choices.
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
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """

        date = self.normalize_datetime(date, output_type='str')

        symbol_type, market = self._change_enum(symbol_type, str), self._change_enum(market, str)
        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = '/v3/reference/tickers'

        _data = {'ticker': symbol, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'type': symbol_type, 'market': market, 'exchange': exchange,
                 'cusip': cusip, 'cik': cik, 'date': date, 'search': search, 'active': active, 'sort': sort,
                 'order': order, 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_ticker_types(self, asset_class=None, locale=None, raw_response: bool = False):
        """
        Get a mapping of ticker types to their descriptive names - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers_types>`__

        :param asset_class: Filter by asset class. see :class:`polygon.enums.AssetClass` for choices
        :param locale: Filter by locale. See :class:`polygon.enums.Locale` for choices
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        asset_class, locale = self._change_enum(asset_class, str), self._change_enum(locale, str)

        _path = '/v3/reference/tickers/types'

        _data = {'asset_class': asset_class,
                 'locale': locale}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_ticker_details(self, symbol: str, date=None, raw_response: bool = False):
        """
        Get a single ticker supported by Polygon.io. This response will have detailed information about the ticker and
        the company behind it.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker>`__

        :param symbol: The ticker symbol of the asset.
        :param date: Specify a point in time to get information about the ticker available on that date. When retrieving
                     information from SEC filings, we compare this date with the period of report date on the SEC
                     filing. Defaults to the most recent available date.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        date = self.normalize_datetime(date, output_type='str')

        _path = f'/v3/reference/tickers/{symbol.upper()}'

        _data = {'date': date}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_bulk_ticker_details(self, symbol: str, from_date=None, to_date=None, custom_dates: list = None,
                                      run_parallel: bool = True, warnings: bool = True, sort='asc',
                                      max_concurrent_workers: int = os.cpu_count() * 5) -> OrderedDict:
        """
        Get ticker details for a symbol for specified date range and/or dates.
        Each response will have detailed information about the ticker and the company behind it (on THAT particular 
        date) `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_tickers__ticker>`__
        
        :param symbol: The ticker symbol to get data for
        :param from_date: The start date of the date range. Must be specified if custom_dates is not supplied
        :param to_date: The end date of the date range. Must be specified if custom_dates is not supplied
        :param custom_dates: A list of dates, for which to get data for. You can specify this WITH a range. Each date 
                             can be a ``date``, ``datetime`` object or a string ``YYYY-MM-DD``
        :param run_parallel: If true (the default), it will use coroutines/tasks to get the responses in
                             parallel. Set to False to get all responses in sequence (will take time)
        :param warnings: Defaults to True which prints warnings. Set to False to disable warnings.
        :param sort: The order of sorting the final results. Defaults to ascending order of dates. See 
                     :class:`polygon.enums.SortOrder` for choices
        :param max_concurrent_workers: This is only used if run_parallel is set to true. Controls how many worker
                                       coroutines are spawned in the internal thread pool. Defaults to 
                                       ``your cpu core count * 5``
        :return: An OrderedDict where keys are dates, and values are corresponding ticker details.
        """
        
        if custom_dates is None:
            if from_date is None or to_date is None:
                raise ValueError('You must supply either custom_dates or (from_date and to_date)')
            else:
                all_dates = self.get_dates_between(from_date, to_date)
        else:
            custom_dates = [self.normalize_datetime(dt, output_type='date') for dt in custom_dates]
            all_dates = sorted(list(set(custom_dates + self.get_dates_between(from_date, to_date))))
            
        # Start off with the requests
        tasks, final_results, sort_order = OrderedDict(), OrderedDict(), self._change_enum(sort, str)
        
        if run_parallel:  # parallel run
            semaphore = asyncio.Semaphore(max_concurrent_workers)
            
            for dt in all_dates:
                tasks[dt] = asyncio.create_task(self.aw_task(self.get_ticker_details(symbol, dt), semaphore))
                
            await asyncio.gather(*tasks.values())

            for task in tasks:
                if isinstance(tasks[task].result(), dict):
                    final_results[task] = tasks[task].result()
                else:
                    if warnings:
                        print(f'Could not get data for {symbol} on {task}. Returned: {tasks[task].result()}')
                        
                    final_results[task] = None

            return final_results if sort_order == 'asc' else OrderedDict(reversed(list(final_results.items())))
        
        # Sequential Run
        for dt in all_dates:
            try:
                data = await self.get_ticker_details(symbol, dt)
                final_results[dt] = data
            except Exception as exc:
                if warnings:
                    print(f'Could not get data for {symbol} on {dt}. Exception: {str(exc)}')
                    
                final_results[dt] = None
            
        return final_results if sort_order == 'asc' else OrderedDict(reversed(list(final_results.items())))

    async def get_option_contract(self, ticker: str, as_of_date=None, raw_response: bool = False):
        """
        get Info about an option contract
        `Official Docs <https://polygon.io/docs/options/get_v3_reference_options_contracts__options_ticker>`__

        :param ticker: An option ticker in standard format. The lib provides `easy functions
                       <https://polygon.readthedocs.io/en/latest/Options.html#creating-option-symbols>`__
                       to build and work with option symbols
        :param as_of_date: Specify a point in time for the contract. You can pass a ``datetime`` or ``date`` object or
                           a string in format ``YYYY-MM-DD``. Defaults to today's date
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        as_of_date = self.normalize_datetime(as_of_date, output_type='str')

        _path = f'/v3/reference/options/contracts/{ensure_prefix(ticker)}'

        _data = {'as_of': as_of_date}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_option_contracts(self, underlying_ticker: str = None, ticker: str = None, contract_type=None,
                                   expiration_date=None, expiration_date_lt=None, expiration_date_lte=None,
                                   expiration_date_gt=None, expiration_date_gte=None, order='asc',
                                   sort='expiration_date', limit=1000, all_pages: bool = False,
                                   max_pages: int = None, merge_all_pages: bool = True, verbose: bool = False,
                                   raw_page_responses: bool = False, raw_response: bool = False):
        """
        List currently active options contracts
        `Official Docs <https://polygon.io/docs/options/get_v3_reference_options_contracts>`__

        :param underlying_ticker: Query for contracts relating to an underlying stock ticker.
        :param ticker: Query for a contract by option ticker.
        :param contract_type: Query by the type of contract. see :class:`polygon.enums.OptionsContractType` for choices
        :param expiration_date: Query by contract expiration date. either ``datetime``, ``date`` or string
                                ``YYYY-MM-DD``
        :param expiration_date_lt: expiration date less than given value
        :param expiration_date_lte: expiration date less than equal to given value
        :param expiration_date_gt: expiration_date greater than given value
        :param expiration_date_gte: expiration_date greater than equal to given value
        :param order: Order of results. See :class:`polygon.enums.SortOrder` for choices.
        :param sort: Sort field for ordering. See :class:`polygon.enums.OptionsContractsSortType` for choices.
                     defaults to expiration_date
        :param limit: Limit the size of the response, default is 1000.
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
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary. This is ignored if pagination is set to True.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object.
                 If pagination is set to True, will return a merged response of all pages for convenience.
        """
        expiration_date = self.normalize_datetime(expiration_date, output_type='str')

        expiration_date_lt = self.normalize_datetime(expiration_date_lt, output_type='str')

        expiration_date_lte = self.normalize_datetime(expiration_date_lte, output_type='str')

        expiration_date_gt = self.normalize_datetime(expiration_date_gt, output_type='str')

        expiration_date_gte = self.normalize_datetime(expiration_date_gte, output_type='str')

        contract_type = self._change_enum(contract_type, str)
        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = f'/v3/reference/options/contracts'

        _data = {'ticker': ticker, 'underlying_ticker': underlying_ticker, 'contract_type': contract_type,
                 'expiration_date': expiration_date, 'expiration_date.lt': expiration_date_lt,
                 'expiration_date.lte': expiration_date_lte, 'expiration_date.gt': expiration_date_gt,
                 'expiration_date.gte': expiration_date_gte, 'order': order, 'sort': sort, 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_ticker_news(self, symbol: str = None, limit: int = 1000, order='desc',
                              sort='published_utc', ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None,
                              published_utc=None, published_utc_lt=None, published_utc_lte=None,
                              published_utc_gt=None, published_utc_gte=None, all_pages: bool = False,
                              max_pages: int = None, merge_all_pages: bool = True, verbose: bool = False,
                              raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get the most recent news articles relating to a stock ticker symbol, including a summary of the article and a
        link to the original source - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v2_reference_news>`__

        :param symbol: To get news mentioning the name given. Defaults to empty string which doesn't filter tickers
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param order: Order the results. See :class:`polygon.enums.SortOrder` for choices.
        :param sort: The field key to sort. See :class:`polygon.enums.TickerNewsSort` for choices.
        :param ticker_lt: Return results where this field is less than the value.
        :param ticker_lte: Return results where this field is less than or equal to the value.
        :param ticker_gt: Return results where this field is greater than the value
        :param ticker_gte: Return results where this field is greater than or equal to the value.
        :param published_utc: A date string ``YYYY-MM-DD`` or ``datetime`` for published date time filters.
        :param published_utc_lt: Return results where this field is less than the value given
        :param published_utc_lte: Return results where this field is less than or equal to the value given
        :param published_utc_gt: Return results where this field is greater than the value given
        :param published_utc_gte: Return results where this field is greater than or equal to the value given
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

        published_utc = self.normalize_datetime(published_utc, output_type='str')

        published_utc_lt = self.normalize_datetime(published_utc_lt)

        published_utc_lte = self.normalize_datetime(published_utc_lte)

        published_utc_gt = self.normalize_datetime(published_utc_gt)

        published_utc_gte = self.normalize_datetime(published_utc_gte)

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = '/v2/reference/news'

        _data = {'limit': limit, 'order': order, 'sort': sort, 'ticker': symbol, 'ticker.lt': ticker_lt,
                 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt, 'ticker.gte': ticker_gte,
                 'published_utc': published_utc, 'published_utc.lt': published_utc_lt,
                 'published_utc.lte': published_utc_lte, 'published_utc.gt': published_utc_gt,
                 'published_utc.gte': published_utc_gte}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_stock_dividends(self, ticker: str = None, ex_dividend_date=None, record_date=None,
                                  declaration_date=None, pay_date=None, frequency: int = None, limit: int = 1000,
                                  cash_amount=None, dividend_type=None, sort: str = 'pay_date', order: str = 'asc',
                                  ticker_lt=None, ticker_lte=None, ticker_gt=None, ticker_gte=None,
                                  ex_dividend_date_lt=None, ex_dividend_date_lte=None, ex_dividend_date_gt=None,
                                  ex_dividend_date_gte=None, record_date_lt=None, record_date_lte=None,
                                  record_date_gt=None, record_date_gte=None, declaration_date_lt=None,
                                  declaration_date_lte=None, declaration_date_gt=None, declaration_date_gte=None,
                                  pay_date_lt=None, pay_date_lte=None, pay_date_gt=None, pay_date_gte=None,
                                  cash_amount_lt=None, cash_amount_lte=None, cash_amount_gt=None, cash_amount_gte=None,
                                  all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                                  verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get a list of historical cash dividends, including the ticker symbol, declaration date, ex-dividend date,
        record date, pay date, frequency, and amount.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_dividends>`__

        :param ticker: Return the dividends that contain this ticker.
        :param ex_dividend_date: Query by ex-dividend date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param record_date: Query by record date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param declaration_date: Query by declaration date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param pay_date: Query by pay date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param frequency: Query by the number of times per year the dividend is paid out. No default value applied.
                          see :class:`polygon.enums.PayoutFrequency` for choices
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param cash_amount: Query by the cash amount of the dividend.
        :param dividend_type: Query by the type of dividend. See :class:`polygon.enums.DividendType` for choices
        :param sort: sort key used for ordering. See :class:`polygon.enums.DividendSort` for choices.
        :param order: orders of results. defaults to asc. see :class:`polygon.enums.SortOrder` for choices
        :param ticker_lt: filter where ticker is less than given value (alphabetically)
        :param ticker_lte: filter where ticker is less than or equal to given value (alphabetically)
        :param ticker_gt: filter where ticker is greater than given value (alphabetically)
        :param ticker_gte: filter where ticker is greater than or equal to given value (alphabetically)
        :param ex_dividend_date_lt: filter where ex-div date is less than given date
        :param ex_dividend_date_lte: filter where ex-div date is less than or equal to given date
        :param ex_dividend_date_gt: filter where ex-div date is greater than given date
        :param ex_dividend_date_gte: filter where ex-div date is greater than or equal to given date
        :param record_date_lt: filter where record date is less than given date
        :param record_date_lte: filter where record date is less than or equal to given date
        :param record_date_gt: filter where record date is greater than given date
        :param record_date_gte: filter where record date is greater than or equal to given date
        :param declaration_date_lt: filter where declaration date is less than given date
        :param declaration_date_lte: filter where declaration date is less than or equal to given date
        :param declaration_date_gt: filter where declaration date is greater than given date
        :param declaration_date_gte: filter where declaration date is greater than or equal to given date
        :param pay_date_lt: filter where pay date is less than given date
        :param pay_date_lte: filter where pay date is less than or equal to given date
        :param pay_date_gt: filter where pay date is greater than given date
        :param pay_date_gte: filter where pay date is greater than or equal to given date
        :param cash_amount_lt: filter where cash amt is less than given value
        :param cash_amount_lte: filter where cash amt is less than or equal to given value
        :param cash_amount_gt: filter where cash amt is greater than given value
        :param cash_amount_gte: filter where cash amt is greater than or equal to given value
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

        ex_dividend_date = self.normalize_datetime(ex_dividend_date, output_type='str')

        record_date = self.normalize_datetime(record_date, output_type='str')

        declaration_date = self.normalize_datetime(declaration_date, output_type='str')

        pay_date = self.normalize_datetime(pay_date, output_type='str')

        ex_dividend_date_lt = self.normalize_datetime(ex_dividend_date_lt, output_type='str')

        ex_dividend_date_lte = self.normalize_datetime(ex_dividend_date_lte, output_type='str')

        ex_dividend_date_gt = self.normalize_datetime(ex_dividend_date_gt, output_type='str')

        ex_dividend_date_gte = self.normalize_datetime(ex_dividend_date_gte, output_type='str')

        record_date_lt = self.normalize_datetime(record_date_lt, output_type='str')

        record_date_lte = self.normalize_datetime(record_date_lte, output_type='str')

        record_date_gt = self.normalize_datetime(record_date_gt, output_type='str')

        record_date_gte = self.normalize_datetime(record_date_gte, output_type='str')

        declaration_date_lt = self.normalize_datetime(declaration_date_lt, output_type='str')

        declaration_date_lte = self.normalize_datetime(declaration_date_lte, output_type='str')

        declaration_date_gt = self.normalize_datetime(declaration_date_gt, output_type='str')

        declaration_date_gte = self.normalize_datetime(declaration_date_gte, output_type='str')

        pay_date_lt = self.normalize_datetime(pay_date_lt, output_type='str')

        pay_date_lte = self.normalize_datetime(pay_date_lte, output_type='str')

        pay_date_gt = self.normalize_datetime(pay_date_gt, output_type='str')

        pay_date_gte = self.normalize_datetime(pay_date_gte, output_type='str')

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)
        frequency, dividend_type = self._change_enum(frequency, int), self._change_enum(dividend_type, str)

        _path = f'/v3/reference/dividends'

        _data = {'ticker': ticker, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'ex_dividend_date': ex_dividend_date,
                 'ex_dividend_date.lt': ex_dividend_date_lt, 'ex_dividend_date.lte': ex_dividend_date_lte,
                 'ex_dividend_date.gt': ex_dividend_date_gt, 'ex_dividend_date.gte': ex_dividend_date_gte,
                 'record_date': record_date, 'record_date.lt': record_date_lt, 'record_date.lte': record_date_lte,
                 'record_date.gt': record_date_gt, 'record_date.gte': record_date_gte,
                 'declaration_date': declaration_date, 'declaration_date.lt': declaration_date_lt,
                 'declaration_date.lte': declaration_date_lte, 'declaration_date.gt': declaration_date_gt,
                 'declaration_date.gte': declaration_date_gte, 'pay_date': pay_date, 'pay_date.lt': pay_date_lt,
                 'pay_date.lte': pay_date_lte, 'pay_date.gt': pay_date_gt, 'pay_date.gte': pay_date_gte,
                 'frequency': frequency, 'cash_amount': cash_amount, 'cash_amount.lt': cash_amount_lt,
                 'cash_amount.lte': cash_amount_lte, 'cash_amount.gt': cash_amount_gt,
                 'cash_amount.gte': cash_amount_gte, 'dividend_type': dividend_type, 'order': order, 'sort': sort,
                 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_stock_financials_vx(self, ticker: str = None, cik: str = None, company_name: str = None,
                                      company_name_search: str = None, sic: str = None, filing_date=None,
                                      filing_date_lt=None, filing_date_lte=None, filing_date_gt=None,
                                      filing_date_gte=None, period_of_report_date=None,
                                      period_of_report_date_lt=None, period_of_report_date_lte=None,
                                      period_of_report_date_gt=None, period_of_report_date_gte=None,
                                      time_frame=None, include_sources: bool = False, order='asc',
                                      limit: int = 50, sort='filing_date', raw_response: bool = False):
        """
        Get historical financial data for a stock ticker. The financials data is extracted from XBRL from company SEC
        filings using `this methodology <http://xbrl.squarespace.com/understanding-sec-xbrl-financi/>`__ - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_vx_reference_financials>`__

        This API is experimental and will replace :meth:`get_stock_financials` in future.

        :param ticker: Filter query by company ticker.
        :param cik: filter the Query by ``central index key (CIK)`` Number
        :param company_name: filter the query by company name
        :param company_name_search: partial match text search for company names
        :param sic: Query by ``standard industrial classification (SIC)``
        :param filing_date: Query by the date when the filing with financials data was filed. ``datetime/date`` or
                            string ``YYYY-MM-DD``
        :param filing_date_lt: filter for filing date less than given value
        :param filing_date_lte: filter for filing date less than equal to given value
        :param filing_date_gt: filter for filing date greater than given value
        :param filing_date_gte: filter for filing date greater than equal to given value
        :param period_of_report_date: query by The period of report for the filing with financials data.
                                      ``datetime/date`` or string in format: ``YYY-MM-DD``.
        :param period_of_report_date_lt: filter for period of report date less than given value
        :param period_of_report_date_lte: filter for period of report date less than equal to given value
        :param period_of_report_date_gt: filter for period of report date greater than given value
        :param period_of_report_date_gte: filter for period of report date greater than equal to given value
        :param time_frame: Query by timeframe. Annual financials originate from 10-K filings, and quarterly financials
                           originate from 10-Q filings. Note: Most companies do not file quarterly reports for Q4 and
                           instead include those financials in their annual report, so some companies my not return
                           quarterly financials for Q4. See :class:`polygon.enums.StockFinancialsTimeframe` for choices.
        :param include_sources: Whether or not to include the xpath and formula attributes for each financial data
                                point. See the xpath and formula response attributes for more info. ``False`` by default
        :param order: Order results based on the sort field. 'asc' by default. See :class:`polygon.enums.SortOrder`
                      for choices.
        :param limit: number of max results to obtain. defaults to 50.
        :param sort: Sort field key used for ordering. 'filing_date' default. see
                     :class:`polygon.enums.StockFinancialsSortKey` for choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        filing_date = self.normalize_datetime(filing_date, output_type='str')

        period_of_report_date = self.normalize_datetime(period_of_report_date, output_type='str')

        filing_date_lt = self.normalize_datetime(filing_date_lt, output_type='str')

        filing_date_lte = self.normalize_datetime(filing_date_lte, output_type='str')

        filing_date_gt = self.normalize_datetime(filing_date_gt, output_type='str')

        filing_date_gte = self.normalize_datetime(filing_date_gte, output_type='str')

        period_of_report_date_lt = self.normalize_datetime(period_of_report_date_lt, output_type='str')

        period_of_report_date_lte = self.normalize_datetime(period_of_report_date_lte, output_type='str')

        period_of_report_date_gt = self.normalize_datetime(period_of_report_date_gt, output_type='str')

        period_of_report_date_gte = self.normalize_datetime(period_of_report_date_gte, output_type='str')

        time_frame = self._change_enum(time_frame)
        order, sort = self._change_enum(order), self._change_enum(sort)

        _path = f'/vX/reference/financials'

        _data = {'ticker': ticker, 'cik': cik, 'company_name': company_name,
                 'company_name_search': company_name_search, 'sic': sic, 'filing_date': filing_date,
                 'filing_date.lt': filing_date_lt, 'filing_date.lte': filing_date_lte,
                 'filing_date.gt': filing_date_gt, 'filing_date.gte': filing_date_gte,
                 'period_of_report_date': period_of_report_date, 'period_of_report_date.lt': period_of_report_date_lt,
                 'period_of_report_date.lte': period_of_report_date_lte,
                 'period_of_report_date.gt': period_of_report_date_gt,
                 'period_of_report_date.gte': period_of_report_date_gte, 'timeframe': time_frame, 'order': order,
                 'include_sources': 'true' if include_sources else 'false', 'limit': limit, 'sort': sort}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_stock_splits(self, ticker: str = None, execution_date=None, reverse_split: bool = None,
                               order: str = 'asc', sort: str = 'execution_date', limit: int = 1000, ticker_lt=None,
                               ticker_lte=None, ticker_gt=None, ticker_gte=None, execution_date_lt=None,
                               execution_date_lte=None, execution_date_gt=None, execution_date_gte=None,
                               all_pages: bool = False, max_pages: int = None, merge_all_pages: bool = True,
                               verbose: bool = False, raw_page_responses: bool = False, raw_response: bool = False):
        """
        Get a list of historical stock splits, including the ticker symbol, the execution date, and the factors of
        the split ratio.
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_splits>`__

        :param ticker: Return the stock splits that contain this ticker. defaults to no ticker filter returning all.
        :param execution_date: query by execution date. could be a date, datetime object or a string ``YYYY-MM-DD``
        :param reverse_split: Query for reverse stock splits. A split ratio where split_from is greater than split_to
               represents a reverse split. By default this filter is not used.
        :param order: Order results based on the sort field. defaults to ascending. See
               :class:`polygon.enums.SortOrder` for choices
        :param sort: Sort field used for ordering. Defaults to 'execution_date'. See
               :class:`polygon.enums.SplitsSortKey` for choices.
        :param limit: Limit the size of the response, default is 1000 which is also the max.
                      ``Pagination`` is supported by the pagination function below
        :param ticker_lt: filter where ticker name is less than given value (alphabetically)
        :param ticker_lte: filter where ticker name is less than or equal to given value (alphabetically)
        :param ticker_gt: filter where ticker name is greater than given value (alphabetically)
        :param ticker_gte: filter where ticker name is greater than or equal to given value (alphabetically)
        :param execution_date_lt: filter where execution date is less than given value
        :param execution_date_lte: filter where execution date is less than or equal to given value
        :param execution_date_gt: filter where execution date is greater than given value
        :param execution_date_gte: filter where execution date is greater than or equal to given value
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

        execution_date = self.normalize_datetime(execution_date, output_type='str')

        execution_date_lt = self.normalize_datetime(execution_date_lt, output_type='str')

        execution_date_lte = self.normalize_datetime(execution_date_lte, output_type='str')

        execution_date_gt = self.normalize_datetime(execution_date_gt, output_type='str')

        execution_date_gte = self.normalize_datetime(execution_date_gte, output_type='str')

        sort, order = self._change_enum(sort, str), self._change_enum(order, str)

        _path = f'/v3/reference/splits'

        _data = {'ticker': ticker, 'ticker.lt': ticker_lt, 'ticker.lte': ticker_lte, 'ticker.gt': ticker_gt,
                 'ticker.gte': ticker_gte, 'execution_date': execution_date, 'execution_date.lt': execution_date_lt,
                 'execution_date.lte': execution_date_lte, 'execution_date.gt': execution_date_gt,
                 'execution_date.gte': execution_date_gte, 'reverse_split': reverse_split, 'order': order,
                 'sort': sort, 'limit': limit}

        _res = await self._get_response(_path, params=_data)

        if not all_pages:  # don't you dare paginating!!
            if raw_response:
                return _res

            return _res.json()

        return await self._paginate(_res, merge_all_pages, max_pages, verbose=verbose,
                                    raw_page_responses=raw_page_responses)

    async def get_market_holidays(self, raw_response: bool = False):
        """
        Get upcoming market holidays and their open/close times - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v1_marketstatus_upcoming>`__

        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = '/v1/marketstatus/upcoming'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_market_status(self, raw_response: bool = False):
        """
        Get the current trading status of the exchanges and overall financial markets - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v1_marketstatus_now>`__

        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        _path = '/v1/marketstatus/now'

        _res = await self._get_response(_path)

        if raw_response:
            return _res

        return _res.json()

    async def get_conditions(self, asset_class=None, data_type=None, condition_id=None, sip=None, order=None,
                             limit: int = 50, sort='name', raw_response: bool = False):
        """
        List all conditions that Polygon.io uses - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_conditions>`__

        :param asset_class: Filter for conditions within a given asset class. See :class:`polygon.enums.AssetClass`
                            for choices. Defaults to all assets.
        :param data_type: Filter by data type. See :class:`polygon.enums.ConditionsDataType` for choices. defaults to
                          all.
        :param condition_id: Filter for conditions with a given ID
        :param sip: Filter by SIP. If the condition contains a mapping for that SIP, the condition will be returned.
        :param order: Order results. See :class:`polygon.enums.SortOrder` for choices.
        :param limit: limit the number of results. defaults to 50.
        :param sort: Sort field used for ordering. Defaults to 'name'. See :class:`polygon.enums.ConditionsSortKey`
                     for choices.
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """
        asset_class, data_type = self._change_enum(asset_class), self._change_enum(data_type)
        order, sort = self._change_enum(order), self._change_enum(sort)

        _path = f'/v3/reference/conditions'

        _data = {'asset_class': asset_class, 'data_type': data_type, 'id': condition_id, 'sip': sip, 'order': order,
                 'limit': limit, 'sort': sort}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()

    async def get_exchanges(self, asset_class=None, locale=None, raw_response: bool = False):
        """
        List all exchanges that Polygon.io knows about - Async method
        `Official Docs <https://polygon.io/docs/stocks/get_v3_reference_exchanges>`__

        :param asset_class: filter by asset class. See :class:`polygon.enums.AssetClass` for choices.
        :param locale: Filter by locale name. See :class:`polygon.enums.Locale`
        :param raw_response: Whether or not to return the ``Response`` Object. Useful for when you need to say check the
                             status code or inspect the headers. Defaults to False which returns the json decoded
                             dictionary.
        :return: A JSON decoded Dictionary by default. Make ``raw_response=True`` to get underlying response object
        """

        asset_class, locale = self._change_enum(asset_class), self._change_enum(locale)

        _path = f'/v3/reference/exchanges'

        _data = {'asset_class': asset_class, 'locale': locale}

        _res = await self._get_response(_path, params=_data)

        if raw_response:
            return _res

        return _res.json()


# ========================================================= #


def ensure_prefix(symbol: str):
    """
    Ensure that the option symbol has the prefix ``O:`` as needed by polygon endpoints. If it does, make no changes. If
    it doesn't, add the prefix and return the new value.

    :param symbol: the option symbol to check
    """
    if len(symbol) < 15:
        raise ValueError('Option symbol length must at least be 15 letters. See documentation on option symbols for '
                         'more info')

    if symbol.upper().startswith('O:'):
        return symbol.upper()

    return f'O:{symbol.upper()}'


# ========================================================= #


if __name__ == '__main__':
    print('Don\'t You Dare Running Lib Files Directly')

# ========================================================= #
