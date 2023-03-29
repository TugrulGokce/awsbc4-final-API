import boto3


class DBWriter:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Arbitrage')

    def write(self, message):
        self.table.put_item(Item={'id': message[0],
                                  'ts': message[1],
                                  'smarket': message[2],
                                  'price': message[3]})
