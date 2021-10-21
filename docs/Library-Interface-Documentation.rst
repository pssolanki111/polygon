

.. _lib_interface_doc_header:

+++++++++++++++++++++++++++++++
Library Interface Documentation
+++++++++++++++++++++++++++++++

Here is the Entire Library Interface reference.

.. _stocks_client_interface_header:

Stocks Client
-------------
.. autoclass:: polygon.stocks.stocks.StocksClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _options_client_interface_header:

Options Client
--------------

.. autofunction:: polygon.options.options.build_option_symbol

.. autofunction:: polygon.options.options.parse_option_symbol

.. autofunction:: polygon.options.options.build_option_symbol_for_tda

.. autofunction:: polygon.options.options.parse_option_symbol_from_tda

.. autoclass:: polygon.options.options.OptionSymbol
   :members:
   :special-members: __init__
   :undoc-members:
   :private-members:
   :member-order: bysource

.. autoclass:: polygon.options.options.OptionsClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. autofunction:: polygon.options.options.ensure_prefix

.. _references_client_interface_header:

References Client
-----------------
.. autoclass:: polygon.reference_apis.reference_api.ReferenceClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _forex_client_interface_header:

Forex Client
------------
.. autoclass:: polygon.forex.forex_api.ForexClient
   :members:
   :special-members: __init__
   :private-members:
   :member-order: bysource

.. _crypto_client_interface_header:

Crypto Client
-------------
.. autoclass:: polygon.crypto.crypto_api.CryptoClient
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
