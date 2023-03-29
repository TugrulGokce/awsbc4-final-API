import json


class Configurator:
    def __init__(self):
        self.cfg = self.load_json()
        self.stock_cfg = self.cfg["StockMarkets"]

    def get_stockmarkets(self):
        return list(self.stock_cfg.keys())

    def get_url(self, param):
        return self.stock_cfg[param]["url"]

    def get_request(self, param):
        return self.stock_cfg[param]["request"]

    def load_json(self, path="configuration.json"):
        with open(path) as config:
            return json.loads(config.read())
