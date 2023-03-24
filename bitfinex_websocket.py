import asyncio
import websockets
import json


async def subscribe_bit_finex():
    url = "wss://api-pub.bitfinex.com/ws/2"
    count = 0
    async with websockets.connect(url) as ws:
        subscribe_request = {
            "event": "subscribe",
            "channel": "trades",
            "symbol": "tBTCUSD"
        }
        await ws.send(json.dumps(subscribe_request))
        while True:
            response = await ws.recv()
            count += 1
            if count > 2:
                data_list = json.loads(response)
                print(data_list)
                if data_list[1] == 'te':
                    print(f"price = {data_list[2][3]}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(subscribe_bit_finex())
