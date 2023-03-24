import asyncio
import websockets
import json


# TODO bazı websocketlerde time olarak unixtimestamp var bazılarında düz tarih var hangi formatta db'ye kaydolacak
# TODO gate.io icin unixtimestamp
async def subscribe_gate_io():
    url = "wss://api.gateio.ws/ws/v4/"
    async with websockets.connect(url) as websocket:
        subscribe_request = {
            "channel": "spot.trades",
            "event": "subscribe",  # "unsubscribe" for unsubscription
            "payload": ["BTC_USDT"]
        }
        await websocket.send(json.dumps(subscribe_request))
        while True:
            response = await websocket.recv()
            print(response)
            data_list = json.loads(response)
            print(data_list)
            if data_list['event'] == 'update':
                print(f"trade_pairs : {data_list['result']['currency_pair']} | price : {data_list['result']['price']} "
                      f"| time : {data_list['time']}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(subscribe_gate_io())
