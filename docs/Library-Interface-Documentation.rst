

.. _lib_interface_doc_header:

+++++++++++++++++++++++++++++++
Library Interface Documentation
+++++++++++++++++++++++++++++++

Here is the Entire Library Interface reference.

.. _base_client_interface_header:

Base Clients
------------

Base Client
~~~~~~~~~~~

.. autoclass:: polygon.base_client.Base
   :members:
   :special-members: __init__
   :private-members:
   :undoc-members:
   :member-order: bysource

Base Sync Client
~~~~~~~~~~~~~~~~

.. autoclass:: polygon.base_client.BaseClient
   :members:
   :special-members: __init__
   :private-members:
   :undoc-members:
   :member-order: bysource

Base Async Client
~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.base_client.BaseAsyncClient
   :members:
   :special-members: __init__
   :private-members:
   :undoc-members:
   :member-order: bysource

.. _stocks_client_interface_header:

Stocks Clients
--------------

Stocks Sync Client
~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.stocks.stocks.SyncStocksClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

Stocks Async Client
~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.stocks.stocks.AsyncStocksClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _options_client_interface_header:

Options Clients
---------------

Option Symbol Helper Functions & Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: polygon.options.options.build_option_symbol

.. autofunction:: polygon.options.options.parse_option_symbol

.. autofunction:: polygon.options.options.build_option_symbol_for_tda

.. autofunction:: polygon.options.options.parse_option_symbol_from_tda

.. autofunction:: polygon.options.options.convert_from_tda_to_polygon_format

.. autofunction:: polygon.options.options.convert_from_polygon_to_tda_format

.. autofunction:: polygon.options.options.detect_symbol_format

.. autofunction:: polygon.options.options.ensure_prefix

.. autoclass:: polygon.options.options.OptionSymbol
   :members:
   :special-members: __init__, __repr__
   :undoc-members:
   :private-members:
   :member-order: bysource

Options Sync Client
~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.options.options.SyncOptionsClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

Options Async Client
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.options.options.AsyncOptionsClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _references_client_interface_header:

References Clients
------------------

Reference Sync Client
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.reference_apis.reference_api.SyncReferenceClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

Reference Async Client
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.reference_apis.reference_api.AsyncReferenceClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _forex_client_interface_header:

Forex Clients
-------------

Forex Sync Client
~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.forex.forex_api.SyncForexClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

Forex Async Client
~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.forex.forex_api.AsyncForexClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _crypto_client_interface_header:

Crypto Clients
--------------

Crypto Sync Client
~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.crypto.crypto_api.SyncCryptoClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

Crypto Async Client
~~~~~~~~~~~~~~~~~~~

.. autoclass:: polygon.crypto.crypto_api.AsyncCryptoClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _callback_streamer_client_interface_header:

Callback Streamer Client (Sync)
-------------------------------
.. autoclass:: polygon.streaming.streaming.StreamClient
   :members:
   :special-members: __init__
   :private-members:
   :undoc-members:
   :member-order: bysource

.. _async_streamer_client_interface_header:

Async Streamer Client
---------------------
.. autoclass:: polygon.streaming.async_streaming.AsyncStreamClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _enums_interface_header:

Enums Interface
---------------

.. automodule:: polygon.enums
   :members:
   :undoc-members:
   :member-order: bysource
