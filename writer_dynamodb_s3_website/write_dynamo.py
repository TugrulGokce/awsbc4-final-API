from writer_dynamodb_s3_website.utils import get_bitfinex_price, get_binance_price, get_gateio_price, get_coinbase_price
from writer_dynamodb_s3_website.db_write import DBWriter
import uuid
import time


def run_write_dynamodb():
    print("Connecting to DB...")
    db = DBWriter()
    print("Connected to DB.")
    while True:
        response = str(uuid.uuid1()), \
            str(time.time())[:10], \
            get_coinbase_price(), \
            get_gateio_price(), \
            get_binance_price(), \
            get_bitfinex_price()
        print("Response :", response)
        db.write(response)
        time.sleep(1)
