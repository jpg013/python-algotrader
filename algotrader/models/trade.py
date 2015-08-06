class Trade():
    def __init__(self, tradeType, stockSymbol, openDate):
        self.tradeType = tradeType
        self.stockSymbol = stockSymbol
        self.openDate = openDate

    def getSaveableObject(self):
        saveable = {}
        saveable['trade_type'] = self.tradeType
        saveable['stock_symbol'] = self.stockSymbol
        saveable['open_date'] = self.openDate
        return saveable
