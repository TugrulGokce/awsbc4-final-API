import json
import boto3
import time

def lambda_handler(event, context):
    current_ts = time.time() - 9_000_000
    dynamodb = boto3.client('dynamodb')
    
    response = dynamodb.scan(
        TableName='arbitrage_btc',
        FilterExpression='ts >= :current_ts',
        ExpressionAttributeValues={
            ':current_ts': {'S': str(current_ts)}
        }
    )

    items = response['Items']
    items.sort(key=lambda x: x["ts"]["S"], reverse=True)
    
    bitfinex_btc, gateio_btc, coinbase_btc = [], [], []
    for i in items[:500]:
        ts = int(i['ts']['S']) * 1000
        if i['bitfinex_btc']:
            bitfinex_btc.append([ts, float(i['bitfinex_btc']['S'])])
        if i['gateio_btc']:
            gateio_btc.append([ts, float(i['gateio_btc']['S'])])
        if i['coinbase_btc']:
            coinbase_btc.append([ts, float(i['coinbase_btc']['S'])])
    
    result = [{'name': 'gateio', 'data': gateio_btc},
              {'name': 'bitfinex', 'data': bitfinex_btc},
              {'name': 'coinbase', 'data': coinbase_btc}]
    
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(result)
    }
