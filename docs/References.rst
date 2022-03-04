
.. _references_header:

Reference APIs
==============

Read this page to know everything you need to know about using the various References HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  reference_client = polygon.ReferenceClient('KEY')  # for usual sync client
  async_reference_client = polygon.ReferenceClient('KEY', True)  # for an async client

here is how the client initializer looks like:

.. autofunction:: polygon.reference_apis.reference_api.ReferenceClient

**Endpoints**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_tickers`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Tickers
-----------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_tickers
   :noindex:

Get Ticker Types
----------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_ticker_types
   :noindex:


Get Ticker Details
------------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_ticker_details
   :noindex:

Get Option Contracts
--------------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_option_contracts
   :noindex:

Get Ticker News
---------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_ticker_news
   :noindex:

Get Stock dividends
-------------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_stock_dividends
   :noindex:

Get Stock financials vX
-----------------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_stock_financials_vx
   :noindex:

Get Stock Splits
----------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_stock_splits
   :noindex:

Get Market Holidays
-------------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_market_holidays
   :noindex:

Get Market Status
-----------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_market_status
   :noindex:

Get Condition Mappings
----------------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_condition_mappings
   :noindex:

Get Conditions
--------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_conditions
   :noindex:

Get Exchanges
-------------

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_exchanges
   :noindex:

