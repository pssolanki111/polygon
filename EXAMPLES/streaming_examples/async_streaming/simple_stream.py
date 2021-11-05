import asyncio
import polygon
from polygon.enums import StreamCluster


async def stock_trades_handler(msg):  # it is possible to create one common message handler for different services.
    print(f'msg received: {msg}')


async def stock_aggregates_handler(msg):
    print(f'aggregate msg: {msg}')


async def main():
    api_key = 'YOUR_KEY'

    stream_client = polygon.AsyncStreamClient(api_key, StreamCluster.STOCKS)

    await stream_client.subscribe_stock_trades(handler_function=stock_trades_handler)  # ALL tickers
    await stream_client.subscribe_stock_second_aggregates(['AMD', 'NVDA'], stock_aggregates_handler)

    while 1:
        await stream_client.handle_messages()  # the lib provides auto reconnect functionality. See docs for info


if __name__ == '__main__':
    asyncio.run(main())

