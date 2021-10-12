# `polygon`: A Polygon.io API Wrapper

## what is `polygon`
`polygon` is a Complete Python Wrapper for [Polygon.io APIs](https://polygon.io/). It offers 
simple and elegant programmatic access over each endpoint. Functionalities include but not limited to:

-  Stocks and Options data
-  Forex and Crypto data
-  Websocket streaming (both callback and async based)
-  Market Info, News, Holidays, Schedules
-  Async support for REST endpoints

and more...

## How do I use `polygon`

The complete description of everything you need to know is available in the [Documentation](https://polygon.readthedocs.io/)

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
    
    current_price = await stocks_client.async_get_current_price('AMD')
    print(current_price)

if __name__ == '__main__':
    asyncio.run(main())
```

### A streaming example (callback based)

```python
import polygon
from polygon.enums import StreamCluster

def my_own_message_handler(msg):
    print(f'Look at me! I\'m the Handler now...: {msg}')

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
    print(f'Look at me! I am the new handler. {msg}')
    
async def main():
    api_key = 'YOUR_KEY'
    
    stream_client = polygon.AsyncStreamClient(api_key, StreamCluster.STOCKS)
    
    await stream_client.subscribe_stock_trades(['AMD', 'NVDA'], stock_trades_handler)
    
    while 1:
        await stream_client.handle_messages()  # the lib provides auto reconnect functionality. See docs for info
if __name__ == '__main__':
    asyncio.run(main())

```

**See the [Documentation](https://polygon.readthedocs.io/) to start using the library with its full functionalities.**

## what if I need help?

See [Getting Help](https://polygon.readthedocs.io/en/latest/getting_help.html)

## anything else?

Bug reports, suggestions and pull requests are always welcome. 

See [Contributing](https://polygon.readthedocs.io/en/latest/contrib_and_license.html)
if you wish to contribute.

Read [This](https://polygon.readthedocs.io/en/latest/bugs_discussions_wikis_faqs.html) before raising a bug.

`polygon` is released under the [MIT License](https://github.com/pssolanki111/polygon/blob/main/LICENSE)