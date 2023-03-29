import asyncio
import websockets
import json
import boto3
from loguru import logger


dynamo_db_client = boto3.resource('dynamodb')
table = dynamo_db_client.Table('coinTrade')
logger.success("Succesfully connected to dynamodb")


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
            data_list = json.loads(response)
            # print(data_list)
            if data_list['event'] == 'update':
                table.put_item(
                    Item={
                        'trade_id': data_list['result']['id'],
                        'symbol': data_list['result']['currency_pair'],
                        'price': data_list['result']['price'],
                        'unix_timestamp': data_list['time'],
                        'source': 'gate.io'
                    },
                )
                logger.info(f"Item --> trade_id: {data_list['result']['id']} | "
                            f"trade_pair_name : {data_list['result']['currency_pair']} | "
                            f"price : {data_list['result']['price']} | "
                            f"source : 'source': 'gate.io' | "
                            f"time : {data_list['time']} succesfully added to 'coinTrade' table")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(subscribe_gate_io())
