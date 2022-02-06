
.. _forex_header:

Forex
=====

Read this page to know everything you need to know about using the various Forex HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  forex_client = polygon.ForexClient('KEY')  # for usual sync client
  async_forex_client = polygon.ForexClient('KEY', True)  # for an async client

Note that most endpoints require you to specify the currency pairs as separate symbols (a ``from_symbol`` and a ``to_symbol``).

however a few endpoints require you to supply them as one combined symbol. An example would be the ``get_aggregates_bars`` method.
In those methods, the symbol is expected to have a prefix ``C:`` before the currency symbol names. **but the library allows you to specify the symbol with or without the prefix**.
See the relevant method's docs for more information on what the parameters expect.

here is how the client initializer looks like:

.. autofunction:: polygon.forex.forex_api.ForexClient

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_historic_forex_ticks`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Historic forex ticks
------------------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_historic_forex_ticks
   :noindex:

Get Quotes (NBBO)
-----------------

This endpoint supports pagination. Passing ``all_pages=True`` enabled it. See :ref:`pagination_header` for better info

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_quotes
   :noindex:

Get Last Quote
--------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_last_quote
   :noindex:

Get Aggregate Bars (Candles)
----------------------------

The library added a better aggregate function if you're looking to get data for large time frames at minute/hour granularity.

(for example 15 years historical data , 1 minute candles)

See :ref:`better_aggs_header` for complete details on how to use it well and control how it behaves.

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_aggregate_bars
   :noindex:

Get Grouped Daily Bars (Candles)
--------------------------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_grouped_daily_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_previous_close
   :noindex:

Get Gainers & Losers
--------------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.get_gainers_and_losers
   :noindex:

Real Time currency conversion
-----------------------------

.. automethod:: polygon.forex.forex_api.SyncForexClient.real_time_currency_conversion
   :noindex:
