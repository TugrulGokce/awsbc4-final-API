import json
import requests


def get_gateio_price():
    url = "https://data.gateapi.io/api2/1/ticker/btc_usd"
    response = json.loads(requests.request("GET", url).text)
    return str(round(float(response["last"]), 2))


def get_bitfinex_price():
    try:
        url = "https://api.bitfinex.com/v1/pubticker/btcusd"
        response = requests.request("GET", url)
        return str(round(float(json.loads(response.text)["last_price"]), 2))
    except:
        return None


def get_binance_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.request("GET", url)
        return str(round(float(json.loads(response.text)["price"]), 2))
    except:
        return None


def get_coinbase_price():
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        response = requests.request("GET", url)
        return str(round(float(json.loads(response.text)["data"]["amount"]), 2))
    except:
        return None
