import boto3


class DBWriter:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Arbitrage')

    def write(self, message):
        self.table.put_item(Item={'id': message[0],
                                  'ts': message[1],
                                  'coinbase_btc': message[2],
                                  'gateio_btc': message[3],
                                  'binance_btc': message[4],
                                  'bitfinex_btc': message[5]})
# TODO : Saniye bazında olacak.
# TODO : timestamp integer casting.
# TODO : tek satırda olacak.
