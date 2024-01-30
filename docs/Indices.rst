
.. _indices_header:

Indices
=======

So you have completed the initial steps and are ready to dive deep into endpoints. Read this page to know everything you need to know
about using the various Indices HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  stocks_client = polygon.IndexClient('KEY')  # for usual sync client
  async_stock_client = polygon.IndexClient('KEY', True)  # for an async client

here is how the client initializer looks like:

.. autofunction:: polygon.indices.indices.IndexClient

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_aggregate_bars`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

SMA
---

Simple Moving Average. This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.indices.indices.SyncIndexClient.get_sma
   :noindex:

EMA
---

Exponential Moving Average. This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.indices.indices.SyncIndexClient.get_ema
   :noindex:

RSI
---

Relative Strength Index. This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.indices.indices.SyncIndexClient.get_rsi
   :noindex:

MACD
----

Moving Average Convergence/Divergence. This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.indices.indices.SyncIndexClient.get_macd
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.indices.indices.SyncIndexClient.get_previous_close
   :noindex:

Get Daily Open Close
--------------------

.. automethod:: polygon.indices.indices.SyncIndexClient.get_daily_open_close
   :noindex:

Get Aggregate Bars
------------------
The library added a better aggregate function if you're looking to get data for large time frames at minute/hour granularity.

(for example 15 years historical data , 1 minute candles)

See :ref:`better_aggs_header` for complete details on how to use it well and control how it behaves.

.. automethod:: polygon.indices.indices.SyncIndexClient.get_aggregate_bars
   :noindex:

Get Snapshot
------------

.. automethod:: polygon.indices.indices.SyncIndexClient.get_snapshot
   :noindex:
