
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

Get Historic forex ticks
------------------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_historic_forex_ticks
   :noindex:

Get Last Quote
--------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_last_quote
   :noindex:

Get Aggregate Bars (Candles)
----------------------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_aggregate_bars
   :noindex:

Get Grouped Daily Bars (Candles)
--------------------------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_grouped_daily_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_previous_close
   :noindex:

Get Gainers & Losers
--------------------

.. automethod:: polygon.forex.forex_api.ForexClient.get_gainers_and_losers
   :noindex:

Real Time currency conversion
-----------------------------

.. automethod:: polygon.forex.forex_api.ForexClient.real_time_currency_conversion
   :noindex:
