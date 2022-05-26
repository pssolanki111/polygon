import polygon
from polygon.enums import StreamCluster


def my_own_message_handler(ws, msg):
    print(f"msg received: {msg}")


def main():
    api_key = "YOUR_KEY"

    stream_client = polygon.StreamClient(
        api_key, StreamCluster.STOCKS, on_message=my_own_message_handler
    )
    stream_client.start_stream_thread()
    stream_client.subscribe_stock_trades(["AMD", "NVDA"])
    stream_client.subscribe_stock_second_aggregates()  # ALL tickers


if __name__ == "__main__":
    main()
