import asyncio
import websockets
import json
from pprint import pprint


async def subscribe():
    url = "wss://ws-feed.exchange.coinbase.com"
    async with websockets.connect(url) as ws:
        subscribe_request = {
            "type": "subscribe",
            "product_ids": [
                "BTC-USD"
            ],
            "channels": ["matches"]
        }
        await ws.send(json.dumps(subscribe_request))
        while True:
            response = await ws.recv()
            data_list = json.loads(response)
            if data_list.get("type") == "match":
                print(data_list)
                print(f"price = {data_list['price']}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(subscribe())
