
.. _options_header:

Options
=======

Read this page to know everything you need to know about using the various Options HTTP endpoints.

See :ref:`async_support_header` for asynchronous use cases.

Docs below assume you have already read getting started page and know how to create the client.
If you do not know how to create the client, first see :ref:`create_and_use_header` and create client as below. As always you can have all 5 different clients together.

.. code-block:: python

  import polygon

  options_client = polygon.OptionsClient('KEY')  # for usual sync client
  async_options_client = polygon.OptionsClient('KEY', True)  # for an async client

here is how the client initializer looks like:

.. autofunction:: polygon.options.options.OptionsClient

**NOTE:** if you don't want to use the option symbol helper functions, then you can just go to the desired endpoint documentation from the list to left

.. _option_symbols_header:

Working with Option Symbols
---------------------------

So when you're working with options (rest/websockets), you'll certainly need the option symbols which contain the information about their underlying symbol, expiry, call_or_put and the
strike price in a certain format. There are many formats to represent them and every data source/brokerage uses a 
different format to represent them.

for example Polygon.io tends to use `This Format <https://www.optionstaxguy.com/option-symbols-osi>`__ . For those who want to understand how this formatting works,
`Here is a guide <https://docs.google.com/document/d/15WYmleETJwB2S80vuj8muWr6DNBIFmcmiB_UmHTosFg/edit>`__ (thanks to Ian from polygon support team).

The library is equipped with a few functions to make it easier for you to **build, parse, convert, and detect 
format** of option symbols without worrying about how the structure works.

This section has been written again following many changes in v1.0.8. If you were using option symbology in v1.0.7 or
older, the documentation for that version is available [here](https://polygon.readthedocs.io/en/1.0.7/) although I'd 
suggest upgrading and making required (small) changes

The library supports the following symbol formats at the moment

===================  ====================
  Full Name            Shorthand String
===================  ====================
Polygon.io           polygon
Tradier              tradier
Trade Station        trade_station
Interactive Brokers  ibkr
TD Ameritrade        tda
Think Or Swim        tos
===================  ====================

This section on option symbols is divided into these sections below. 

1. **Creating** Option symbols from info as underlying, expiry, strike price, option type
#. **Parsing** Option symbols to **extract** info as underlying, expiry, strike price, option type
#. **Converting** an option symbol from one format to another. Works between all supported formats.
#. **Detecting** format of an option symbol. Basic detection based on some simple rules.

Creating Option Symbols
~~~~~~~~~~~~~~~~~~~~~~~

The function in this sub-section helps you to build option symbols from info as underlying symbol, expiry, strike 
price & option type (call/put). The function to use is ``polygon.build_option_symbol``

-  Since the default format is polygon.io you don't need to specify a format if you're only working with polygon 
   option symbols.
-  Polygon has a rest endpoint in reference client to get all active contracts which you can filter based on 
   many values such as underlying symbol and expiry dates.
-  In polygon format, If you wonder whether you need to worry about the ``O:`` prefix which some/all option endpoints 
   expect, then to your ease, the library handles that for you (So you can pass a symbol without prefix to let's say
   Option Snapshot function and the prefix will be added internally). If you want to be explicit, just pass 
   ``prefix_o=True`` when building symbol.
-  Note that both tradier and polygon happen to use the exact same symbol format and hence can be used interchangeably.

Example Code & Output for polygon/tradier format

.. code-block:: python

  import polygon
  
  symbol1 = polygon.build_option_symbol('AMD', datetime.date(2022, 6, 28), 'call', 546.56)
  symbol2 = polygon.build_option_symbol('TSLA', '220628', 'c', 546, _format='polygon')
  symbol3 = polygon.build_option_symbol('A', '220628', 'put', 66.01, prefix_o=True)
  
  # Outputs
  # symbol1 -> AMD220628C00546560
  # symbol2 -> TSLA220628C00546000
  # symbol3 -> O:A220628P00066010
  
  
The same function can be used to create option symbols for any of the supported formats, just pass in the format you 
need, either as a shorthand string from the table above, or use an enum from :class:`polygon.enums.OptionSymbolFormat`

-  Using enums (like ``OptionSymbolFormat.POLYGON`` in example below) is a good way to ensure you only pass in 
   correct shorthand strings. Your IDE auto completion would make your life much easier when working with enums.

Example code & outputs for multiple formats

.. code-block:: python

  from polygon import build_option_symbol  # you can import the way you like, just showing the alternates
  from polygon.enums import OptionSymbolFormat  # optional, you can pass in shorthand strings too
  
  symbol1 = polygon.build_option_symbol('AMD', datetime.date(2022, 6, 28), 'call', 546.56, _format='tda')
  symbol2 = polygon.build_option_symbol('NVDA', '220628', 'c', 546, _format='tos')
  symbol3 = polygon.build_option_symbol('TSLA', datetime.date(2022, 6, 28), 'put', 46.01, _format='tradier')
  symbol4 = polygon.build_option_symbol('A', datetime.date(2022, 6, 28), 'p', 46.1, _format='ibkr')
  symbol5 = polygon.build_option_symbol('AB', datetime.date(2022, 6, 28), 'p', 46.01, _format='trade_station')
  symbol6 = polygon.build_option_symbol('PTON', '220628', 'p', 46, _format=OptionSymbolFormat.POLYGON)  # using enum
  
  # outputs
  # symbol1 -> AMD_062822C546.56
  # symbol2 -> .NVDA062822C546
  # symbol3 -> TSLA220628P00046010
  # symbol4 -> A 220628P00046100
  # symbol5 -> AB 220628P46.01
  # symbol5 -> PTON220628P00046000

For those who want more control, here is how the function signature and arguments look

.. autofunction:: polygon.options.options.build_option_symbol
   :noindex:

Parsing Option Symbols
~~~~~~~~~~~~~~~~~~~~~~

The function in this sub-section helps you to extract info as underlying symbol, expiry, strike price & option type  
(call/put) from an existing option symbol. Parsing is available on all supported formats. The function to use is 
``polygon.build_option_symbol``

-  Since the default format is ``polygon``, you don't need to specify a format if you're only working with polygon 
   option symbols.
-  Polygon symbols can be passed in with or without the prefix ``O:``. Library will handle both internally
-  Note that both tradier and polygon happen to use the exact same symbol format and hence can be used interchangeably.
-  It is observed that some option symbols as returned by polygon endpoints happen to have a **correction number** 
   within the symbol. The additional number is always between the underlying symbol and expiry. 
   **The lib handles that for you** & parses the symbol accordingly.
-  An example of the corrected polygon symbol could be ``XY1221015C00234000``. Notice the extra 1 after ``XY`` and 
   before expiry ``221015``. The library would parse this symbol as ``XY221015C00234000``. The number could be any 
   number according to a response from polygon support team.

**NOTE:** The parse function takes another optional argument, ``output_format``, defaulting to ``'object'``. 
Here is what it is for and how you can use it to your advantage.

Output Format
 The library provides 3 possible output formats when getting parsed info from an option symbol. They are

-  An object of class :class:`polygon.options.options.OptionSymbol` (Default). You can access info as 

  *  ``obj.strike_price``
  *  ``obj.underlying_symbol``
  *  ``obj.expiry``
  *  ``obj.call_or_put``
  *  ``obj.option_symbol``

-  As a list having elements: ``[underlying_symbol, expiry, call_or_put, strike_price, option_symbol]`` in this fixed
   order
-  As a dict having the following keys:

  *  ``underlying_symbol``
  *  ``expiry``
  *  ``call_or_put``
  *  ``strike_price``
  *  ``option_symbol``


Example code and output for polygon/tradier formats

.. code-block:: python

  import polygon
  
  parsed_details1 = polygon.parse_option_symbol('AMD211205C00156000')
  parsed_details2 = polygon.parse_option_symbol('AMD211205C00156000', output_format=list)
  parsed_details3 = polygon.parse_option_symbol('AMD211205C00156000', output_format=dict)
  
  # outputs
  # parsed_details1 would be an object having info as attributes as described in output format sub-section above
  # parsed_details2 -> ['AMD', dt.date(2021, 12, 5), 'C', 156, 'AMD211205C00156000']
  # parsed_details3 -> {'underlying_symbol': 'AMD', 'expiry': dt.date(2021, 12, 5), 'call_or_put': 'C',  'strike_price': 156, 'option_symbol': 'AMD211205C00156000'}

The same function can be used to parse option symbols in any of the supported formats, just pass in the format you 
need, either as a shorthand string from the table above, or use an enum from :class:`polygon.enums.OptionSymbolFormat`

-  Using enums (like ``OptionSymbolFormat.POLYGON`` in example below) is a good way to ensure you only pass in 
   correct shorthand strings. Your IDE auto completion would make your life much easier when working with enums.

Example code & outputs for multiple formats

.. code-block:: python

  import polygon
  
  parsed_details1 = polygon.parse_option_symbol('AMD211205C00156000', _format='tradier')
  parsed_details2 = polygon.parse_option_symbol('AMD_062822P587.56', _format='tda', output_format=list)
  parsed_details3 = polygon.parse_option_symbol('AB 220628P46.01', _format='trade_station', output_format=dict)
  
  # outputs
  # parsed_details1 would be an object having info as attributes as described in output format sub-section above
  # parsed_details2 -> ['AMD', dt.date(2022, 6, 28), 'P', 587.56, 'AMD_062822P587.56']
  # parsed_details3 -> {'underlying_symbol': 'AB', 'expiry': dt.date(2022, 6, 28), 'call_or_put': 'P', 'strike_price': 46.01, 'option_symbol': 'AB 220628P46.01'}

For those who want more control, here is how the function signature and arguments look

.. autofunction:: polygon.options.options.parse_option_symbol
   :noindex:

Converting Option Symbol Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function in this sub-section helps you to convert an option symbol from one format to another. So if you want to 
convert a polygon option symbol to TD Ameritrade symbol (say to place an order), pass the symbol in this function, 
specify the formats and the library will do the conversions for you.

Example code and outputs

.. code-block:: python

  import polygon
  
  symbol1 = polygon.convert_option_symbol_formats('AMD220628P00096050', from_format='polygon', to_format='tda')
  symbol2 = polygon.convert_option_symbol_formats('AB 220628P46.01', from_format='trade_station', to_format='polygon')
  symbol2 = polygon.convert_option_symbol_formats('NVDA220628C00546000', 'tradier', 'tos')
  
  # outputs
  # symbol1 -> AMD_062822P96.05
  # symbol2 -> AB220628P00046010
  # symbol3 -> .NVDA062822C546
  
For those who want more control, here is how the function signature and arguments look

.. autofunction:: polygon.options.options.convert_option_symbol_formats
   :noindex:

Detecting Option Symbol Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function in this sub-section helps you to detect the symbol format of an option symbol programmatically. The 
function does basic detection according to some simple rules so test well before using this in production setting. It
is almost always recommended to be explicit about formats.

Example code and outputs

.. code-block:: python

  import polygon
  
  format1 = polygon.detect_option_symbol_format('AMD_062822P96.05')
  format2 = polygon.detect_option_symbol_format('AB220628P00046010')
  format3 = polygon.detect_option_symbol_format('.NVDA062822C546')
  format4 = polygon.detect_option_symbol_format('AB 220628P46.01')
  format5 = polygon.detect_option_symbol_format('AB 220628P00046045')
  
  # outputs
  # format1 -> 'tda'
  # format2 -> 'polygon'  # this also means tradier since both use exact same format
  # format3 -> 'tos'
  # format4 -> 'trade_station'
  # format5 -> ['ibkr', 'trade_station']

For those who want more control, here is how the function signature and arguments look

.. autofunction:: polygon.options.options.detect_option_symbol_format
   :noindex:

.. _option_endpoints_header:


**Endpoints:**

To use any of the below method, simply call it on the client you created above. so if you named your client ``client``,
you'd call the methods as ``client.get_trades`` and so on. Async methods will need to be awaited, see :ref:`async_support_header`.

Get Trades
----------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_trades
   :noindex:

Get Quotes
----------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_quotes
   :noindex:

Get Last Trade
--------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_last_trade
   :noindex:

Get Daily Open Close
--------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_daily_open_close
   :noindex:

Get Aggregate Bars
------------------

The library added a better aggregate function if you're looking to get data for large time frames at minute/hour granularity.

(for example 15 years historical data , 1 minute candles)

See :ref:`better_aggs_header` for complete details on how to use it well and control how it behaves.

.. automethod:: polygon.options.options.SyncOptionsClient.get_aggregate_bars
   :noindex:

Get Previous Close
------------------

.. automethod:: polygon.options.options.SyncOptionsClient.get_previous_close
   :noindex:

Get Snapshot
------------

This endpoint supports pagination. Passing ``all_pages=True`` enables it. See :ref:`pagination_header` for better info

.. automethod:: polygon.options.options.SyncOptionsClient.get_snapshot
   :noindex:
