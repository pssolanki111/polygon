
.. _stocks_header:

Stocks
======

So you have completed the initial steps and are ready to dive deep into endpoints. Read this page to know everything you need to know
about using the various Stocks HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  stocks_client = polygon.StocksClient('KEY')  # for usual sync client
  async_stock_client = polygon.StocksClient('KEY', True)  # for an async client

here is how the client initializer looks like:

.. autofunction:: polygon.stocks.stocks.StocksClient

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_trades`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Trades
----------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_trades
   :noindex:

Get Trades v3
-------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_trades_v3
   :noindex:

Get Quotes
----------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_quotes
   :noindex:

Get Quotes v3
-------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_quotes_v3
   :noindex:

Get Last Trade
--------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_last_trade
   :noindex:

Get last Quote
--------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_last_quote
   :noindex:

Get Daily Open Close
--------------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_daily_open_close
   :noindex:

Get Aggregate Bars (Candles)
----------------------------

The library added a better aggregate function if you're looking to get data for large time frames at minute/hour granularity.

(for example 15 years historical data , 1 minute candles)

See :ref:`better_aggs_header` for complete details on how to use it well and control how it behaves.

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_aggregate_bars
   :noindex:

Get Grouped daily Bars (Candles)
--------------------------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_grouped_daily_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_previous_close
   :noindex:

Get Snapshot
------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_snapshot
   :noindex:

Get Snapshot (All)
------------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_snapshot_all
   :noindex:

Get Current Price
-----------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_current_price
   :noindex:

Get Gainers & Losers
--------------------

.. automethod:: polygon.stocks.stocks.SyncStocksClient.get_gainers_and_losers
   :noindex:


