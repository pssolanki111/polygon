
.. _bulk_data_download_header:

Bulk Data Download Functions
============================

This page documents all the bulk data download functions the library offers. New functions are added 
based on community feedback. 

To suggest a bulk download function which might be useful to be in the lib, 
join our `Discord Server <https://discord.gg/jPkARduU6N>`__

Below is a short description of the available bulk data functions in the library

=====================  ====================
  Name                    Summary
=====================  ====================
Full Range Aggregates  Historical OCHLV candles for a large duration
Bulk Ticker Details    Ticker Details for a date range
=====================  ====================

.. _better_aggs_header:

Bulk Aggregate Bars (Full Range)
--------------------------------

Available on both regular and async clients, this function makes it easy to get historical price history (OCHLV 
candles) for a large duration. For example **One Minute candles for AMD for the past 15 years**

How does the function work
~~~~~~~~~~~~~~~~~~~~~~~~~~

Skip if you don't care :D

- This function attempts to work around the 50k candles' limit set by polygon. 50k is enough for 1 month duration, but
  not for 15 years as you can tell
- The library splits your specified date range into smaller chunks of time, gets data for them in parallel 
  (threads/coroutines) or sequential (if you say so), merges all responses, drops duplicates & candles outside the 
  specified range and finally returns a single list of all candles.

General Advice
~~~~~~~~~~~~~~

- If you are looking to use this functionality for MANY symbols (read more than 4-5), then it is better to use the 
  async client. Due to GIL limitation in python, regular client can't run more than 1 threadpool at a time.
- For most people, the default values should be enough, but for the ones who hate themselves ( :P ), it is possible to
  customize the behavior however they like.
- The concept is the same for all clients (stocks, options, forex and crypto). Knowing it once is 
  enough for all other clients as they all have same method names.

Enough Talking, Show me how to use it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may call this function in two ways,

-  Calling the usual ``client.get_aggregate_bars()`` method and passing ``full_range=True``.
-  Directly calling ``client.get_full_range_aggregate_bars()`` (added in ``v1.0.9``)

for example the below two calls are identical

.. code-block:: python
   
   # 'client' can be any client out of stocks, options, forex & crypto.
   client.get_aggregate_bars('AMD', '2005-06-28', '2022-06-28', full_range=True)
   
   # same effect as above, different call (added in v1.0.9)
   client.get_full_range_aggregate_bars('AMD', '2005-06-28', '2022-06-28')
   
The output format is a **single list of all candles**.
   
Now that you know how to use it, below is info on how to customize how the function runs, to suit your architecture and 
requirements

-  By default: library runs an internal Threadpool (regular sync client) OR a set of coroutines (async client). Both 
   run different smaller time chunks in parallel.

-  If you don't want it to run in parallel (not recommended), you can just specify ``run_parallel=False``. doing that 
   will make the library request data one by one, using the last response received as the new start point until end 
   date is reached. This might be useful if you're running a thread pool of your own and don't want the internal
   thread pool to mess with your own thread pool. **on async client, always prefer to run parallel**

-  In parallel (default) style run, if you deal with an asset which trades for a higher number hours in a day, you can 
   add the additional argument ``smaller_time_chunks=True``. This will make the library further reduce its time chunk size.
   This argument was renamed from ``high_volatility`` to ``smaller_time_chunks`` in **v1.0.9**

-  By default, function will also print some warnings if they occur. You can turn off those warnings using 
   ``warnings=False``.

-  When working with the parallel versions, you also have the ability to specify how many concurrent threads/coroutines you wish to spawn using ``max_concurrent_workers=a new number``
   ONLY change it if you know you need it. This can sometimes help reduce loads or gain performance boost.
   The default is ``your cpu core count * 5``

-  By default, the results returned will be in ascending order (oldest candles first in the final output). To change 
   that simply specify descending order. You can either pass an enum 
   :class:`polygon.enums.SortOrder` (recommended) or pass a string ``sort='desc'``.


I want to do it manually, but could use some help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sure. The function used by these functions internally to split a large date range into 
smaller time chunks, is also available to use directly.

It returns a list of time chunks with their respective start and end times. You can then use your own logic to get 
data for those chunks, process and merge it however you like.

The method you want to call is ``client.split_date_range()``, like so:

.. code-block:: python

  import polygon

  client = polygon.StocksClient('KEY')

  time_frames = client.split_date_range('2005-06-28', '2022-06-28', timespan='minute')
  print(time_frames)

-  By default the list returned will have newer timeframes first. To change that, pass ``reverse=False``

-  The argument ``smaller_time_chunks`` is available here too and can be used for assets which are traded a high 
   number of hours in a day. This argument was renamed from ``high_volatility`` to ``smaller_time_chunks`` in **v1.0.9**

Here is the method signature

.. automethod:: polygon.base_client.Base.split_date_range
   :noindex:

.. _bulk_ticker_details_header:

Bulk Ticker Details
-------------------

Available on both regular and async clients, this function makes it easy to get ticker details for a specified 
ticker, for each day in a given date range.

It's useful for quickly collecting data such as **historical outstanding shares for a symbol**. 

How does the function work
~~~~~~~~~~~~~~~~~~~~~~~~~~

Skip if you don't care :D

- This function would generate a final list of dates from the range of dates and/or custom dates.
- The response for all dates is fetched in parallel (threads/coroutines) or sequential (if you say so)
- The function returns an ``OrderedDict`` with the dates as keys and the ticker details as values. 

General Advice
~~~~~~~~~~~~~~

- If you are looking to use this functionality for MANY symbols (read more than 4-5), then it is better to use the 
  async client. Due to GIL limitation in python, regular client can't run more than 1 threadpool at a time.
- For most people, the default values should be enough, but for the ones who hate themselves ( :P ), it is possible to
  customize the behavior however they like.
- The method is ONLY available on ``ReferenceClient`` for obvious reasons.

Enough Talking, Show me how to use it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some example calls:

.. code-block:: python

  res = client.get_bulk_ticker_details('AMD', '2005-06-28', '2022-07-11')
  res = client.get_bulk_ticker_details('AMD', from_date='2005-06-28', to_date='2022-07-11')  # this & above are equivalent
  
  res = client.get_bulk_ticker_details('NVDA', custom_dates=['2005-06-28', '2022-07-20'])  # without date range
  res = client.get_bulk_ticker_details('NVDA', from_date='2005-07-02', to_date='2022-07-11',
                                       custom_dates=['2005-06-28', '2022-07-01'])  # with custom dates and a range
                                       
Return Value
  The function returns an ``OrderedDict`` with the dates as keys and the ticker details as values. Iterating over the
  result would iterate over a fixed order (ascending by default) of the dates. You can set ``sort='desc'`` to reverse.
                                       
Customizing Behavior:

-  When using async client, just await the method call. ``res = await client.get_bulk_ticker_details(...)``
-  You CAN supply both a date range (from-to) and custom_dates. You MUST supply either one of those. Duplicate dates 
   are dropped by the library internally.

-  If you don't want it to run in parallel (not recommended), you can just specify ``run_parallel=False``. doing that 
   will make the library request data one by one. This might be useful if you're running a thread pool of your own 
   and don't want the internal thread pool to mess with your own thread pool.
   **on async client, always prefer to run parallel**

-  By default, function will also print some warnings if they occur. You can turn off those warnings using 
   ``warnings=False``.

-  When working with the parallel versions, you also have the ability to specify how many concurrent threads/coroutines you wish to spawn using ``max_concurrent_workers=a new number``
   ONLY change it if you know you need it. This can sometimes help reduce loads or gain performance boost.
   The default is ``your cpu core count * 5``

Here is the method signature:

.. automethod:: polygon.reference_apis.reference_api.SyncReferenceClient.get_bulk_ticker_details
   :noindex:

I want to do it manually, but could use some help
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sure. The function used to get a list of unique, sorted dates between two dates, is also available to use directly.
Call it like:

.. code-block:: python
    
  # client can be any client instance out of stocks, options, references, forex or crypto
  all_dates = client.get_dates_between('2005-03-08', '2022-06-28')
  all_dates = client.get_dates_between('2005-03-08', '2022-06-29', include_to_date=False)

You can then use your own logic to get data for these dates, process and aggregate them however you like. Here is the
method signature

.. automethod:: polygon.base_client.Base.get_dates_between
   :noindex:
