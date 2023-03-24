import asyncio
import websockets
import json
import boto3
from loguru import logger

# TODO bazı websocketlerde time olarak unixtimestamp var bazılarında düz tarih var hangi formatta db'ye kaydolacak
# TODO gate.io icin unixtimestamp
# TODO dynamodb de partition key ney'e göre olacak.

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
                        'trade_pair_name': data_list['result']['currency_pair'],
                        'price': data_list['result']['price'],
                        'unix_timestamp': data_list['time'],
                    },
                )
                logger.info(f"Item --> trade_id: {data_list['result']['id']} | "
                            f"trade_pair_name : {data_list['result']['currency_pair']} | "
                            f"price : {data_list['result']['price']} | "
                            f"time : {data_list['time']} succesfully added to 'coinTrade' table")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(subscribe_gate_io())
