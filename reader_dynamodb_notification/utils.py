import boto3
import time


class DBReader:
    """
    DB Reader.
    """

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('arbitrage_btc')

    def get_last_min(self):
        current_ts = time.time() - 600
        dynamodb = boto3.client('dynamodb')

        response = dynamodb.scan(
            TableName='arbitrage_btc',
            FilterExpression='ts >= :current_ts',
            ExpressionAttributeValues={
                ':current_ts': {'S': str(current_ts)}
            }
            # ScanIndexForward=True
        )

        items = response['Items']
        return items
