
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

Get Trades
----------

.. automethod:: polygon.stocks.stocks.StocksClient.get_trades

Get Quotes
----------

.. automethod:: polygon.stocks.stocks.StocksClient.get_quotes

Get Last Trade
--------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_last_trade

Get last Quote
--------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_last_quote

Get Daily Open Close
--------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_daily_open_close

Get Aggregate Bars (Candles)
----------------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_aggregate_bars

Get Grouped daily Bars (Candles)
--------------------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_grouped_daily_bars

Get Previous Close
------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_previous_close

Get Snapshot
------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_snapshot

Get Snapshot (All)
------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_snapshot_all

Get Current Price
-----------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_current_price

Get Gainers & Losers
--------------------

.. automethod:: polygon.stocks.stocks.StocksClient.get_gainers_and_losers


Note on Async Methods
=====================

All async methods basically have the same name as above except having ``async_`` in the beginning of the name.

so ``async_get_trades``, ``async_get_snapshot`` and so on...

See :ref:`async_support_header` for guide on how to use them.


