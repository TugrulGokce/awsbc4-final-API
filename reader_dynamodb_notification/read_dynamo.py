import pandas as pd
import time
from reader_dynamodb_notification.utils import DBReader


def run_read_dynamo_sns(diff_usd, sec):
    db_reader = DBReader()
    while True:

        result = db_reader.get_last_min()

        bitfinex_btc, gateio_btc, binance_btc, coinbase_btc, ts = [], [], [], [], []

        for res in result:
            ts.append(res["ts"]["S"])
            bitfinex_btc.append(res["bitfinex_btc"]["S"])
            gateio_btc.append(res["gateio_btc"]["S"])
            binance_btc.append(res["binance_btc"]["S"])
            coinbase_btc.append(res["coinbase_btc"]["S"])

        df = pd.DataFrame({
            "ts": ts,
            "bitfinex_btc": bitfinex_btc,
            "gateio_btc": gateio_btc,
            "binance_btc": binance_btc,
            "coinbase_btc": coinbase_btc}).astype(float)

        # df = df.astype(float)

        stock_features = ["bitfinex_btc", "gateio_btc", "binance_btc", "coinbase_btc"]
        diff_serie = df[stock_features].max(axis=1) - df[stock_features].min(axis=1)
        max_idx = diff_serie.idxmax()
        max_smarket = df[stock_features].loc[max_idx].idxmax()
        min_smarket = df[stock_features].loc[max_idx].idxmin()

        max_smarket = max_smarket[:max_smarket.find("_")]
        min_smarket = min_smarket[:min_smarket.find("_")]

        max_price = df[stock_features].loc[max_idx].max()
        min_price = df[stock_features].loc[max_idx].min()
        diff_price = round(max_price - min_price, 2)

        if diff_price > diff_usd:
            print(
                f"Dear MSAHIN. BTC prices on {max_smarket} hits ${max_price} and on {min_smarket} hits ${min_price}."
                f"There is an arbitrage opportunity with a difference of ${diff_price}!")
        else:
            print("there is no enough difference")

        time.sleep(sec)
