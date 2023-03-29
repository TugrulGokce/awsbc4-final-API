import asyncio
import websockets
import json
import boto3
from loguru import logger
from configure import Configurator
import time
import datetime
from db_write import DBWriter
import uuid


class CallerAPI:
    def __init__(self):
        self.cfg = Configurator()
        self.db = DBWriter()

    async def are_apis_available(self):
        for smarket in self.cfg.get_stockmarkets():
            async with websockets.connect(self.cfg.get_url(smarket)) as ws:
                await ws.send(json.dumps(self.cfg.get_request(smarket)))
                response = await ws.recv()
                print(f"API is OK -> {smarket}, RESPONSE ->", response)
        return True

    async def start_writing(self, smarket):
        async with websockets.connect(self.cfg.get_url(smarket)) as ws:
            await ws.send(json.dumps(self.cfg.get_request(smarket)))
            while True:
                response = json.loads(await ws.recv())
                if self.is_response(response, smarket):
                    response = self.response_formatter(response, smarket)
                    print(response)
                    self.db.write(response)

    def response_formatter(self, response, smarket):
        # format [ id, ts, ts, smarket, price]

        if smarket == "gateio":
            return str(uuid.uuid1()), self.get_time(), smarket, response["result"]["price"]

        elif smarket == "coinbase":
            return str(uuid.uuid1()), self.get_time(), smarket, response["price"]

        if smarket == "bitfinex":
            return str(uuid.uuid1()), self.get_time(), smarket, response[2][3]

    def is_response(self, response, smarket):
        if smarket == "coinbase":
            if response.get("type") == "match":
                return True

        if smarket == "gateio":
            if response.get("event") == "update":
                return True

        if smarket == "bitfinex":
            if type(response) == list:
                if response[1] == "te":
                    return True

    def get_time(self):
        return str(time.time())
