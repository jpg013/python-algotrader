from algotrader.models import Trend
from decimal import *
getcontext().prec = 7
from algotrader.database import database

class TFDynamic():
    def __init__(self, movingAverage, leastSquaresSlope):
        self.rsiRates = []
        self.movingAverage = movingAverage
        self.currentTrend = None
        self.alpha = Decimal('60')
        self.omega = Decimal('40')
        self.leastSquaresSlope = leastSquaresSlope
        self.leastSquaresInterval = 20

    def run(self, trendPoint):
        if (hasattr(trendPoint, "rsi") and hasattr(trendPoint, "emaRsi")):
            self.rsiRates.append(trendPoint)
            self.trending(trendPoint)

    def trending(self, trendPoint):
        rsi = getattr(trendPoint, 'rsi')
        emaRsi = getattr(trendPoint, 'emaRsi')

        if self.currentTrend != None:
            self.currentTrend.addTrendRate(trendPoint)

        trendAction = self.WhatIsTrendDoing()

        if trendAction == "advancing":
            if rsi > emaRsi:
                if emaRsi < self.omega or emaRsi > self.alpha:
                    if self.currentTrend is None:
                        self.currentTrend = Trend(self.rsiRates, "dynamic", "upward", self.movingAverage, trendPoint)
                        print("opening upward dynamic trend")
                    else:
                        trendDirection = getattr(self.currentTrend, "direction")
                        if trendDirection is "downward":
                            database.saveTrend(self.currentTrend)
                            self.currentTrend = None
                            self.rsiRates = []
                            print("Closing dynamic downward trend")
        elif trendAction == "retreating":
            if rsi < emaRsi:
                if emaRsi < self.omega or emaRsi > self.alpha:
                    if self.currentTrend is None:
                        self.currentTrend = Trend(self.rsiRates, "dynamic", "downward", self.movingAverage, trendPoint)
                        print("Opening downward dynamic trend")
                    else:
                        trendDirection = getattr(self.currentTrend, "direction")
                        if trendDirection is "upward":
                            database.saveTrend(self.currentTrend)
                            self.currentTrend = None
                            self.rsiRates = []
                            print("Closing dynamic upward trend")

    # Use Least Square Method to determine whether trending upward or downward
    def WhatIsTrendDoing(self):
        if (len(self.rsiRates) < self.leastSquaresInterval):
            return "nothing"

        recentRates = self.rsiRates[-1 * self.leastSquaresInterval:]
        xSum = Decimal('0') # Time Values
        ySum = Decimal('0') # CloseMid Values
        for rate in recentRates:
            xSum += Decimal(str(rate.time))
            ySum += rate.closeMid

        xBar = xSum / Decimal(str(len(recentRates)))
        yBar = ySum / Decimal(str(len(recentRates)))

        slopeNum = Decimal('0')
        slopeDen = Decimal('0')
        for rate in recentRates:
            x = Decimal(str(rate.time)) - xBar
            slopeNum += (x * (rate.closeMid - yBar))
            slopeDen += x ** 2

        slope = slopeNum / slopeDen

        if slope > self.leastSquaresSlope:
            return "advancing"
        elif slope < (self.leastSquaresSlope * Decimal('-1')):
            return "retreating"
        else:
            return "nothing"
