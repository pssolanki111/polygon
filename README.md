# `polygon`: A Polygon.io API Wrapper

[![Discord](https://img.shields.io/discord/903351697995337820)](https://discord.gg/jPkARduU6N) [![Documentation Status](https://readthedocs.org/projects/polygon/badge/?version=latest)](https://polygon.readthedocs.io/en/latest/Getting-Started.html) [![pypi](https://img.shields.io/pypi/v/polygon?label=latest%20version)](https://pypi.org/project/polygon/) [![CodeFactor](https://www.codefactor.io/repository/github/pssolanki111/polygon/badge/main)](https://www.codefactor.io/repository/github/pssolanki111/polygon/overview/main) [![ff](https://img.shields.io/github/issues-raw/pssolanki111/polygon)](https://github.com/pssolanki111/polygon/issues) [![fd](https://img.shields.io/github/contributors/pssolanki111/polygon)](https://github.com/pssolanki111/polygon/graphs/contributors) [![Licensess](https://img.shields.io/pypi/l/polygon)](https://github.com/pssolanki111/polygon/blob/main/LICENSE) [![gh](https://img.shields.io/github/followers/pssolanki111?label=Github%20Follows)](https://github.com/pssolanki111)                                                          

## what is `polygon`
`polygon` is a Complete Python Wrapper for [Polygon.io APIs](https://polygon.io/). It offers 
simple and elegant programmatic access over each endpoint. Functionalities include but not limited to:

-  Stocks and Options data
-  Forex and Crypto data
-  Websocket streaming (both callback and async based)
-  Market Info, News, Holidays, Schedules
-  Async support for REST endpoints
-  Built In stream reconnection functionality (only async stream, callback stream in progress)
-  Pagination support (next/previous pages)

and more...

## How do I use `polygon`

The complete description of everything you need to know is available in the [Documentation](https://polygon.readthedocs.io/en/latest/Getting-Started.html) which has answers to 
any question you might have with example uses included wherever needed. Docs is a must-read for most people.

More examples will be added to this repository in a folder `examples` as they are ready. 

### Here is a quick setup guide with a few examples

Before you do anything, you'll need to have a polygon account and get your API key. 
Visit [your dashboard](https://polygon.io/dashboard/api-keys) to get your API key.

Next, you'd need to install `polygon`

```shell
pip install polygon
```

**and You're good to Go!** A few quick examples.

### Getting a stock's current market price

```python
import polygon

api_key = 'YOUR_KEY'

stocks_client = polygon.StocksClient(api_key)

current_price = stocks_client.get_current_price('AMD')

print(current_price)
```

### An Async example for REST endpoints - current price

```python
import polygon
import asyncio

async def main():
    api_key = 'YOUR_KEY'
    
    stocks_client = polygon.StocksClient(api_key, True)
    
    current_price = await stocks_client.get_current_price('AMD')
    await stocks_client.close()  # Recommended to close the httpx session when it's not needed. 
    print(current_price)

if __name__ == '__main__':
    asyncio.run(main())
```

### A streaming example (callback based)

```python
import polygon
from polygon.enums import StreamCluster

def my_own_message_handler(ws, msg):
    print(f'msg received: {msg}')

def main():
    api_key = 'YOUR_KEY'

    stream_client = polygon.StreamClient(api_key, StreamCluster.STOCKS, on_message=my_own_message_handler)
    stream_client.start_stream_thread()
    stream_client.subscribe_stock_trades(['AMD', 'NVDA'])

if __name__ == '__main__':
    main()
```
### An Async streaming example

```python
import asyncio
import polygon
from polygon.enums import StreamCluster

async def stock_trades_handler(msg):   # it is possible to create one common message handler for different services.
    print(f'msg received: {msg}')
    
async def main():
    api_key = 'YOUR_KEY'
    
    stream_client = polygon.AsyncStreamClient(api_key, StreamCluster.STOCKS)
    
    await stream_client.subscribe_stock_trades(['AMD', 'NVDA'], stock_trades_handler)
    
    while 1:
        await stream_client.handle_messages()  # the lib provides auto reconnect functionality. See docs for info
if __name__ == '__main__':
    asyncio.run(main())

```
This only scratches the surface of the library.

**See the [Documentation](https://polygon.readthedocs.io/) to start using the library with its full functionalities.**

## what if I need help?

We have a [Discord Server](https://discord.gg/jPkARduU6N). Join in to ask a question, share your ideas or observations or to just chat with
interesting people, maybe just for lurking :eyes:

See [Getting Help](https://polygon.readthedocs.io/en/latest/getting_help.html) or you can also [start a quick discussion](https://github.com/pssolanki111/polygon/discussions)

## Quick Links for `Speed Runners`

-  [Getting Started](https://polygon.readthedocs.io/en/latest/Getting-Started.html) - a must-read for almost everyone
-  [Async support for REST endpoints](https://polygon.readthedocs.io/en/latest/Getting-Started.html#async-support-for-rest-endpoints)  || [Pagination Support](https://polygon.readthedocs.io/en/latest/Getting-Started.html#pagination-support)
-  Documentation for all [Stocks APIs](https://polygon.readthedocs.io/en/latest/Stocks.html) || [Options APIs](https://polygon.readthedocs.io/en/latest/Options.html) || [Reference APIs](https://polygon.readthedocs.io/en/latest/References.html)
-  Documentation for all [Forex APIs](https://polygon.readthedocs.io/en/latest/Forex.html) || [Crypto APIs](https://polygon.readthedocs.io/en/latest/Crypto.html)
-  Documentation for [Callback Streaming](https://polygon.readthedocs.io/en/latest/Callback-Streaming.html) || [Async Streaming](https://polygon.readthedocs.io/en/latest/Async-Streaming.html)
-  [Easy guide to enums](https://polygon.readthedocs.io/en/latest/using_enums.html) || [Library Interface Docs](https://polygon.readthedocs.io/en/latest/Library-Interface-Documentation.html)
-  [Docs on bugs, discussions, wikis and FAQs](https://polygon.readthedocs.io/en/latest/bugs_discussions_wikis_faqs.html)
-  [Contribution and License](https://polygon.readthedocs.io/en/latest/Library-Interface-Documentation.html)

## Anything else?

Bug reports, suggestions and pull requests are always welcome. 

See [Contributing](https://polygon.readthedocs.io/en/latest/contrib_and_license.html)
if you wish to contribute.

Read [This](https://polygon.readthedocs.io/en/latest/bugs_discussions_wikis_faqs.html) before raising a bug.

`polygon` is released under the [MIT License](https://github.com/pssolanki111/polygon/blob/main/LICENSE)