import json
import boto3
import time
import csv
import io
from datetime import datetime


def lambda_handler(event, context):
    current_ts = time.time() - 900
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(("datetime", "bitfinex_btc", "binance_btc", "coinbase_btc", "gateio_btc"))

    items.sort(key=lambda x: x["ts"]["S"])

    for item in items[:250]:
        writer.writerow(
            (
                datetime.fromtimestamp(int(item["ts"]["S"])),
                item["bitfinex_btc"]["S"],
                item["binance_btc"]["S"],
                item["coinbase_btc"]["S"],
                item["gateio_btc"]["S"]
            )
        )

    # print(output.getvalue())

    # TODO implement
    return {
        'statusCode': 200,
        'body': output.getvalue()  # json.dumps(items)
    }
