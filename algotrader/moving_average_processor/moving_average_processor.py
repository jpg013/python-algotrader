from queue import Queue
from decimal import *
getcontext().prec = 7

class MovingAverageProcessor():
    def __init__(self, intervals):
        self.workers = []
        for interval in intervals:
            self.workers.append(MovingAverageWorker(interval))

    def run(self, rate):
        for worker in self.workers:
            worker.run(rate)

class MovingAverageWorker():
    def __init__(self, interval):
        self.historicalRates = []
        self.lagInterval = interval

    def run(self, rate):
        self.PruneHistoricalRates()

        if (len(self.historicalRates) + 1 ) < self.lagInterval:
            rate.setMovingAverageVal("sma", None)
            rate.setMovingAverageVal("ema", None)
            rate.setMovingAverageVal("smma", None)
            rate.setMovingAverageVal("lwma", None)
        else:
            self.computeSMA(rate)
            self.computeEMA(rate)
            self.computeSMMA(rate)
            self.computeLWMA(rate)

        self.historicalRates.append(rate)

    # Get recent rates from the interval. The historical data
    # does not yet include the current rate, so everything needs
    # to be offset by 1. (e.g. an interval of 10 should return the last 9 rates)
    def PruneHistoricalRates(self):
        offsetInterval = self.lagInterval - 1
        dataLength = len(self.historicalRates)
        if (dataLength < offsetInterval):
            return
        self.historicalRates = self.historicalRates[(-1)*offsetInterval:]

    def computeSMA(self, rate):
        totalSum = Decimal('0')
        for historicalRate in self.historicalRates:
            totalSum += historicalRate.closeMid

        # add in values of current rate
        totalSum += rate.closeMid
        numberPeriods = Decimal(str(len(self.historicalRates) + 1))

        smaVal = totalSum / numberPeriods
        rate.setMovingAverageVal("sma", smaVal)

    def computeEMA(self, rate):
        numberPeriods = Decimal(str(len(self.historicalRates) + 1))
        # Equation for EMA(current) = alpha * (price) + (1 - alpha) * EMA(previous)
        prevEMA = None
        alpha = Decimal('2') / Decimal(str(numberPeriods + 1))
        for historicalRate in self.historicalRates:
            if prevEMA is None:
                smaVal = historicalRate.getMovingAverageVal("sma")
                if smaVal:
                    prevEMA = smaVal # Init EMA to equal SMA of rate for the lag interval
                else:
                    prevEMA = historicalRate.closeMid
            else:
                prevEMA = (alpha * historicalRate.closeMid) + ((1 - alpha) * prevEMA)

        emaVal = (alpha * rate.closeMid) + ((1 - alpha) * prevEMA)
        rate.setMovingAverageVal("ema", emaVal)

    def computeSMMA(self, rate):
        totalSum = Decimal('0')
        for historicalRate in self.historicalRates:
            totalSum += historicalRate.closeMid

        # add in values of current rate
        totalSum += rate.closeMid
        numberPeriods = Decimal(str(len(self.historicalRates) + 1))

        ## Equation for Smoothed Moving Average (SMMA) SMMA(i) = (SUM1 - SMMA1+CLOSE(i))/n
        # https://mahifx.com/indicators/smoothed-moving-average-smma
        smmaSum = totalSum
        smmaOriginal = smmaSum / numberPeriods
        smmaVal = (smmaSum - smmaOriginal + rate.closeMid) / numberPeriods
        rate.setMovingAverageVal("smma", smmaVal)

    def computeLWMA(self, rate):
        # Linear Weighted Moving Average (LWMA)
        #LWMA = SUM(Close(i)*i, N)/SUM(i, N)
        linearSum = Decimal('0')
        linearMultiplier = Decimal('0')
        index = Decimal('1')
        for historicalRate in self.historicalRates:
            linearMultiplier += (historicalRate.closeMid * index)
            linearSum += index
            index += Decimal('1')
        # add in values of current rate
        linearMultiplier += (rate.closeMid * index)
        linearSum += index
        lwmaVal = linearMultiplier / linearSum
        rate.setMovingAverageVal("lwma", lwmaVal)
