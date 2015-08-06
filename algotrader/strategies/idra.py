# Strategy : Get the 5 stocks with the worst previous trading day returns and go long.
from algotrader.workers import RateProcessor
from algotrader.models import Trade
from algotrader.database import database
from datetime import datetime, timedelta
from dateutil import tz

class Idra:
    def __init__(self, end=None, start=None):
        self.holidays = []
        self.rateData = []

        # Load holidays
        self.getHolidays()

        # Load symbols
        self.loadSymbols()

        if end is None:
            end = datetime.today()

        while not self.isValidTradingDay(end):
            end = self.getPreviousTradingDay(end)

        if start is None:
            start = end - timedelta(days=1)

        while not self.isValidTradingDay(start):
            start = self.getPreviousTradingDay(start)

        self.start = start
        self.end = end

        # Load Rate Data
        print "load rate data"
        self.loadRateData()
        print "finished loading rate data"

    # Allocate stock selection
    def allocateStocks(self, rates, capital):
        ret = {}
        eligible = False
        for rate in rate:
            if rate.adjClose <= capital:
                eligible = True
                break

        if not eligible:
            print "No eligible rates to allocate!"
            return

        # Allocation algorithm
        tmp = {}
        while True: # Brute Force



    # Computes daily return for a single day.
    def getStrategyTrades(self, date=None):
        if date is None:
            date = self.end

        print "Get Strategy Trades for date {0}".format(date.date())
        x = self.getNextTradingDay(date)

        filtered  = [rate for rate in self.rateData if rate.date.date() == date.date()]
        dailyReturns = []

        for item in filtered:
            if hasattr(item, 'dailyReturn'):
                dailyReturns.append(item)

        dailyReturns.sort(key=lambda r: r.dailyReturn, reverse=False)

        # Get 5 worst returns
        worstReturns = dailyReturns[:5]
        for item in worstReturns:
            trade = Trade("long", item.symbol, x)
            database.saveTrade(trade)

    def loadRateData(self):
        for symbol in self.symbols:
            print "Loading rate data for {0}".format(symbol)
            rateProcessor = RateProcessor(symbol, self.start, self.end, "d")
            rates = rateProcessor.getRates()
            if len(rates) == 2:
                self.rateData += rates

    def getHolidays(self):
        file = open("./stockmarketholidaytable.csv", "r")
        for line in file:
            items = line.split(",")
            holidayDate = datetime.strptime(items[0], "%Y-%m-%d")
            self.holidays.append(holidayDate)
        file.close()

    def getNextTradingDay(self, date):
        nextTradingDay = date + timedelta(days=1)
        while True:
            if not self.isWeekend(nextTradingDay) and not self.isHoliday(nextTradingDay):
                break
            else:
                nextTradingDay = nextTradingDay + timedelta(days=1)
        return nextTradingDay

    def getPreviousTradingDay(self, date):
        prevTradingDay = date - timedelta(days=1)
        while True:
            if not self.isWeekend(prevTradingDay) and not self.isHoliday(prevTradingDay):
                break
            else:
                prevTradingDay = prevTradingDay - timedelta(days=1)
        return prevTradingDay

    def isValidTradingDay(self, date):
        return not self.isWeekend(date) and not self.isHoliday(date)

    def isWeekend(self, date):
        if date.weekday() > 4:
            return True
        else:
            return False

    def isHoliday(self, date):
        for holiday in self.holidays:
            if date.date() == holiday.date():
                return True
        return False

    def loadSymbols(self):
        self.symbols = []
        data = database.getSymbols()
        for item in data:
            self.symbols.append(item["symbol"])
        self.symbols.sort()

    def isMarketOpen(self):
        from_zone = tz.gettz('America/Chicago')
        to_zone = tz.gettz('America/New_York')
        now = datetime.now()
        central = now.replace(tzinfo=from_zone)
        eastern = central.astimezone(to_zone)
        hour = eastern.hour
        minute = eastern.minute

    def testEquityLine(self, initialInvestment):
        print "testing strategy with investment {0} and percent invested {1}".format(investment, percentInv)

        totalReturns = []

        x = self.start
        while x.date() < self.end.date():
            dailyRates = [rate for rate in self.rateData if rate.date() == x.date()]
            if len(dailyRates) == 0:
                x = x + timedelta(days=1)
                continue
            else:
                dailyReturns = []
                for item in dailyRates:
                    if hasattr(item, 'dailyReturn'):
                        dailyReturns.append(item)

                if len(dailyReturns) > 0:
                    dailyReturns.sort(key=lambda r: r.dailyReturn, reverse=False)
                    worstReturns = dailyReturns[:5]
                    # Worst Returns contains the rates that we are going to buy. We need a brute force algorithm to distribute

        filtered = [rate for rate in self.rateData if rate.date.date() != self.start.date()]
        dailyReturns = []

        for item in filtered:
            if hasattr(item, 'dailyReturn'):
                dailyReturns.append(item)

        dailyReturns.sort(key=lambda r: r.dailyReturn, reverse=False)

        # Get 5 worst returns
        worstReturns = dailyReturns[:5]
        for item in worstReturns:
            trade = Trade("long", item.symbol, x)
            database.saveTrade(trade)

        dailyReturns.sort(key=lambda r: r.dailyReturn, reverse=False)

        for trade in trades:
            openDate = trade["open_date"]
            symbol = trade["stock_symbol"]
            prevDate = self.getPreviousTradingDay(openDate)
            x = None
            y = None
            for rate in self.rateData:
                if rate['date'].date() == openDate.date() and rate['symbol'] == symbol:
                    x = rate
                if rate['date'].date() == prevDate.date() and rate['symbol'] == symbol:
                    y = rate
                if x is not None and y is not None:
                    break

            if x is None:
                print "NOT FOUND"
                continue
            if y is None:
                print "NOT FOUND"
                continue

            dailyReturn = (x['adjClose'] - y['adjClose']) / y['adjClose']
            returns.append(dailyReturn)
        print "Finished with returns"
        return returns
