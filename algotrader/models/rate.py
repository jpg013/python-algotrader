import time
from decimal import *
getcontext().prec = 7

# Fields rateData = {"symbol": self.symbol,"date" : date, "open" : open, "high" : high, "low" : low, "close" : close, "volume" : volume, "adjClose" : adjClose}
class Rate():
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.date = data["date"]
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.volume = data["volume"]
        self.adjClose = data["adjClose"]

    def getSaveableObject(self):
        saveable = {}
        saveable['date'] = self.date
        saveable['symbol'] = self.symbol
        saveable['high'] = self.high
        saveable['low'] = self.low
        saveable['open'] = self.open
        saveable['close'] = self.close
        saveable['volume'] = self.volume
        saveable['adj_close'] = self.adjClose
        return saveable
