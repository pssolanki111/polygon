
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

Get Tickers
-----------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_tickers
   :noindex:

Get Next Page of tickers
------------------------

A simple implementation of pagination on tickers endpoint. Simply pass in the last response you received and the method would parse the
``next_url`` attribute and fetch the next page. If this returns ``False``, it means all pages were fetched.

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_next_page_tickers
   :noindex:

Get Ticker Types
----------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_ticker_types_v3
   :noindex:

Get Ticker Details
------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_ticker_details
   :noindex:

Get Ticker Details vX
---------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_ticker_details_vx
   :noindex:

Get Option Contracts
--------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_option_contracts
   :noindex:

Get next page of option contracts
---------------------------------

A simple implementation of pagination on option contacts endpoint. Simply pass in the last response you received and the method would parse the
``next_url`` attribute and fetch the next page. If this returns ``False``, it means all pages were fetched.

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_next_page_option_contracts
   :noindex:

Get Ticker News
---------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_ticker_news
   :noindex:

Get Next page of ticker news
----------------------------

A simple implementation of pagination on news endpoint. Simply pass in the last response you received and the method would parse the
``next_url`` attribute and fetch the next page. If this returns ``False``, it means all pages were fetched.

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_next_page_news
   :noindex:

Get Stock dividends
-------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_stock_dividends
   :noindex:

Get Stock Financials
--------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_stock_financials
   :noindex:

Get Stock financials vX
-----------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_stock_financials_vx
   :noindex:

Get Stock Splits
----------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_stock_splits
   :noindex:

Get Market Holidays
-------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_market_holidays
   :noindex:

Get Market Status
-----------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_market_status
   :noindex:

Get Condition Mappings
----------------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_condition_mappings
   :noindex:

Get Conditions
--------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_conditions
   :noindex:

Get Exchanges
-------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_exchanges
   :noindex:

Get Locales
-----------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_locales
   :noindex:

Get Markets
-------------

.. automethod:: polygon.reference_apis.reference_api.ReferenceClient.get_markets
   :noindex:

