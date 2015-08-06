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
    rates = database.loadAllRates()
    #rates.sort(key=lambda x: x["date"], reverse = False)
    print rates[0]["date"]
    print rates[-1]["date"]



    print dailyReturns
