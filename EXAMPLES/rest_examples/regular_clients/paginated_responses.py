from polygon import ReferenceClient


KEY = 'API_KEY'

reference_client = ReferenceClient(KEY)

# getting ALL ticker names from polygon

responses = []  # just creating a list to store all responses that we get. You can use your own approach here

response = reference_client.get_tickers(limit=1000)

while 'next_url' in response.keys():
    next_page = reference_client.get_next_page(response)
    responses.append(next_page)

print(f'All pages received. Total pages: {len(responses)}')
