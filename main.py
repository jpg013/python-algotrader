from algotrader.strategies import Idra
from algotrader.workers import RateProcessor
from algotrader.workers import SharpeProcessor
from algotrader.database import database
from datetime import datetime, timedelta
import sys
import json
from bson import json_util

if __name__ == "__main__":
    database.removeTrades()
    #sharpe = SharpeProcessor()
    #longSharpe = sharpe.computeLongSharpe(longRates)
    #longShortSharpe = sharpe.computeLongShortMarketNeutralSharpe(longRates, shortRates)
    #sharpe.computeMaxMinDrawdown(longRates, shortRates)

    # Test last two years of data
    beginDate = datetime.strptime("2015-04-21", "%Y-%m-%d")
    endDate = datetime.today()
    idra = Idra(beginDate, endDate)

    # Test Strategy
    returns = idra.testStrategy()
    longSharpe = sharpe.computeLongSharpe(returns)
    print longSharpe
    print "finished!"
