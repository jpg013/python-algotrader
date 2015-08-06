from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.algotrading
rate_collection = db.rates
trade_collection = db.trades
symbol_collection = db.symbols

def removeRates():
    rate_collection.remove()

def removeTrades():
    trade_collection.remove()

def getTrades():
    trades = trade_collection.find()
    return trades

def loadAllRates():
    index = 0
    rates = []
    for rate in rate_collection.find():
        index += 1
        rates.append(rate)
        print index
    return rates

def getRates(symbol):
    rates = []
    for rate in rate_collection.find({"symbol": symbol}):
        rates.append(rate)
    return rates

def saveRate(rate):
    saveable = rate.getSaveableObject()
    rateId = rate_collection.insert(saveable)
    return rateId

def saveTrade(trade):
    saveable = trade.getSaveableObject()
    trade_collection.insert(saveable)

def getSymbols():
    symbols = []
    for symbol in symbol_collection.find():
        symbols.append(symbol)
    return symbols

def saveSymbol(symbol):
    symbol_collection.insert(symbol)
