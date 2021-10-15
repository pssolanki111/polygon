# ========================================================= #
import unittest
import polygon
from polygon import cred
import datetime
from requests.models import Response
import asyncio
from httpx import Response as HttpxResponse
# ========================================================= #

# Test Runners
cred.KEY = cred.OK

# ========================================================= #


# Helper Function for testing asyncio components
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


# ========================================================= #


class TestOptions(unittest.TestCase):
    def test_get_last_trade(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_last_trade('O:TSLA210903C00700000')
            data2 = client.get_last_trade('O:TSLA210903C00700000', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_last_trade('O:TSLA210903C00700000')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    def test_get_previous_close(self):
        with polygon.OptionsClient(cred.KEY) as client:
            data = client.get_previous_close('O:TSLA210903C00700000')
            data2 = client.get_previous_close('O:TSLA210903C00700000', adjusted=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, Response)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY)
        data = client.get_previous_close('O:TSLA210903C00700000')
        client.close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_last_trade(self):
        async with polygon.OptionsClient(cred.KEY, use_async=True) as client:
            data = await client.async_get_last_trade('O:TSLA210903C00700000')
            data2 = await client.async_get_last_trade('O:TSLA210903C00700000', raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, use_async=True)
        data = await client.async_get_last_trade('O:TSLA210903C00700000')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')

    @async_test
    async def test_async_get_previous_close(self):
        async with polygon.OptionsClient(cred.KEY, use_async=True) as client:
            data = await client.async_get_previous_close('O:TSLA210903C00700000')
            data2 = await client.async_get_previous_close('O:TSLA210903C00700000', adjusted=True, raw_response=True)

            self.assertIsInstance(data, dict)
            self.assertIsInstance(data2, HttpxResponse)

            self.assertIsInstance(data2.json(), dict)

            self.assertEqual(data['status'], 'OK')
            self.assertEqual(data2.json()['status'], 'OK')

        # Testing without context manager
        client = polygon.OptionsClient(cred.KEY, use_async=True)
        data = await client.async_get_previous_close('O:TSLA210903C00700000')
        await client.async_close()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['status'], 'OK')


# ========================================================= #

if __name__ == '__main__':
    unittest.main()

# ========================================================= #
