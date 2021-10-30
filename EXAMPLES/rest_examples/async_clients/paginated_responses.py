from polygon import ReferenceClient
import asyncio

KEY = 'API_KEY'


async def main():
    reference_client = ReferenceClient(KEY, True)

    # getting ALL ticker names from polygon

    responses = []  # just creating a list to store all responses that we get. You can use your own approach here

    response = await reference_client.get_tickers(limit=1000)

    while 'next_url' in response.keys():
        next_page = await reference_client.get_next_page(response)
        responses.append(next_page)

    print(f'All pages received. Total pages: {len(responses)}')


if __name__ == '__main__':
    asyncio.run(main())
