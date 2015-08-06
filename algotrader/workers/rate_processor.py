import datetime
import requests
requests.packages.urllib3.disable_warnings()
from algotrader.models import Rate
from algotrader.database import database

class RateProcessor():
    def __init__(self, symbol, startDate, endDate, period):
        self.rawData = []
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.period = period
        self.run()

    def run(self):
        s = requests.Session()
        a = str(self.startDate.month - 1)
        b = str(self.startDate.day)
        c = str(self.startDate.year)
        d = str(self.endDate.month - 1)
        e = str(self.endDate.day)
        f = str(self.endDate.year)

        url = "http://ichart.yahoo.com/table.csv?s="+self.symbol+"&a="+a+"&b="+b+"&c="+c+"&d="+d+"&e="+e+"&f="+f+"&g="+self.period+"&ignore=.csv"
        req = requests.Request('GET', url)
        pre = req.prepare()
        resp = s.send(pre, stream=False, verify=False)

        if resp.status_code != 200:
            print "fucking error"
            print self.symbol
        else:
            first = True
            for line in resp.iter_lines():
                if first:
                    first = False
                    continue
                if line:
                    tick = line.decode('utf-8').split(",")
                    self.processRawRate(tick)

    def getRates(self):
        print "Getting Rates"
        rates = []
        for data in self.rawData:
            rates.append(Rate(data))
        rates.sort(key=lambda x: x.date, reverse = False)
        print "Processed {0} rates for {1}".format(len(rates), self.symbol)
        self.computeDailyReturns(rates)
        return rates

    def saveRates(self):
        savedCount = 0
        for data in self.rawData:
            r = Rate(data)
            rateId = database.saveRate(r)
            if rateId:
                savedCount += 1
        print "Loaded {0} rates for {1}".format(savedCount, self.symbol)
        return savedCount

    def computeDailyReturns(self, rates):
        for idx, val in enumerate(rates):
            if idx == 0:
                continue
            else:
                prevRate = rates[idx-1]
                dailyReturn = (val.adjClose - prevRate.adjClose)  / prevRate.adjClose
                val.dailyReturn = dailyReturn

    def processRawRate(self, tick):
        date = datetime.datetime.strptime(tick[0], "%Y-%m-%d")
        open = float(tick[1])
        high = float(tick[2])
        low = float(tick[3])
        close = float(tick[4])
        volume = float(tick[5])
        adjClose = float(tick[6])

        rateData = {"symbol": self.symbol,"date" : date, "open" : open, "high" : high, "low" : low, "close" : close, "volume" : volume, "adjClose" : adjClose}
        self.rawData.append(rateData)
