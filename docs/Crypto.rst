
.. _crypto_header:

Crypto
======

Read this page to know everything you need to know about using the various Crypto HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  crypto_client = polygon.CryptoClient('KEY')  # for usual sync client
  async_crypto_client = polygon.CryptoClient('KEY', True)  # for an async client

Get Historic Trades
-------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_historic_trades
   :noindex:

Get Last Trade
-------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_last_trade
   :noindex:

Get Daily Open Close
--------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_daily_open_close
   :noindex:

Get Aggregate Bars (Candles)
----------------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_aggregate_bars
   :noindex:

Get Grouped Daily Bars (Candles)
--------------------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_grouped_daily_bars
   :noindex:

Get Previous Close
-------------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_previous_close
   :noindex:

Get Snapshot All
----------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_snapshot_all
   :noindex:

Get Snapshot
------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_snapshot
   :noindex:

Get Level 2 Book
----------------

.. automethod:: polygon.crypto.crypto_api.CryptoClient.get_level2_book
   :noindex:

