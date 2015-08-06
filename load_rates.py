from algotrader.workers import RateProcessor
from algotrader.database import database
from datetime import datetime

if __name__ == "__main__":
    database.removeRates()
    x = datetime.strptime("2010-01-01", "%Y-%m-%d")
    y = datetime.today()

    symbols = database.getSymbols()
    symbols.sort(key=lambda x: x["symbol"], reverse=False)
    for item in symbols:
        symbol = item["symbol"]
        rateProcessor = RateProcessor(symbol, x, y, "d")
        rateProcessor.saveRates()

    print "FINISHED LOADING RATES"
