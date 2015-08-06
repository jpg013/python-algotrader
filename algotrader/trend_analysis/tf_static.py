from algotrader.models import Trend
from decimal import *
getcontext().prec = 7
from algotrader.database import database

class TFStatic():
    def __init__(self, movingAverage):
        self.upwardTrendLine = []
        self.downwardTrendLine = []
        self.movingAverage = movingAverage
        self.currentTrend = None
        self.delta = Decimal('.00017') # 3 pips
        self.alpha = Decimal('.00002') # 3/10 pip

    def run(self, trendPoint):
        if self.currentTrend is None:
            if self.trendingUpward(trendPoint):
                print("Upward Trend Detected")
            elif self.trendingDownward(trendPoint):
                print("Upward Trend Detected")
        else:
            self.currentTrend.addTrendRate(trendPoint)

            # Check if trend still valid
            if self.currentTrend.direction is "upward":
                trendLine = getattr(self.currentTrend, "trendLine")
                baseline = getattr(self.currentTrend, "baseline")
                baselineTime = getattr(baseline, "time")
                baselineVal = baseline.getMovingAverageVal(self.movingAverage)

                for point in reversed(trendLine):
                    pointTime = getattr(point, "time")
                    if pointTime < baselineTime:
                        break
                    else:
                        trendPointVal = point.getMovingAverageVal(self.movingAverage)
                        spread = baselineVal - trendPointVal
                        if spread >= self.alpha:
                            database.saveTrend(self.currentTrend)
                            self.currentTrend = None

            else:
                trendLine = getattr(self.currentTrend, "trendLine")
                baseline = getattr(self.currentTrend, "baseline")
                baselineTime = getattr(baseline, "time")
                baselineVal = baseline.getMovingAverageVal(self.movingAverage)

                for point in reversed(trendLine):
                    pointTime = getattr(point, "time")
                    if pointTime < baselineTime:
                        break
                    else:
                        trendPointVal = point.getMovingAverageVal(self.movingAverage)
                        spread = trendPointVal - baselineVal
                        if spread >= self.alpha:
                            database.saveTrend(self.currentTrend)
                            self.currentTrend = None

    def trendingUpward(self, trendPoint):
        uptickCount = len(self.upwardTrendLine)
        if (uptickCount == 0):
            self.upwardTrendLine.append(trendPoint)
            return False

        index = self.upwardTrendLine[-1].getMovingAverageVal(self.movingAverage)
        baseline = self.upwardTrendLine[0].getMovingAverageVal(self.movingAverage)

        currIndex = trendPoint.getMovingAverageVal(self.movingAverage)
        if currIndex < index:
            # Trend has dropped below index: disqualify
            self.clearUpwardTrendLine()
            return False
        else:
            self.upwardTrendLine.append(trendPoint)
            spread = currIndex - baseline
            if uptickCount > 2 and spread >= self.delta:
                self.currentTrend = Trend(self.upwardTrendLine, "static", "upward", self.movingAverage)
                return True
            else:
                return False

    def trendingDownward(self, trendPoint):
        downtickCount = len(self.downwardTrendLine)
        if (downtickCount == 0):
            self.downwardTrendLine.append(trendPoint)
            return False

        index = self.downwardTrendLine[-1].getMovingAverageVal(self.movingAverage)
        baseline = self.downwardTrendLine[0].getMovingAverageVal(self.movingAverage)

        currIndex = trendPoint.getMovingAverageVal(self.movingAverage)
        if currIndex > index:
            # Trend has moved above index: disqualify
            self.clearDownwardTrendLine()
            return False
        else:
            self.downwardTrendLine.append(trendPoint)
            spread = baseline - currIndex
            if downtickCount > 2 and spread >= self.delta:
                self.currentTrend = Trend(self.downwardTrendLine, "static", "downward", self.movingAverage)
                return True
            else:
                return False

    def clearUpwardTrendLine(self):
        for point in self.upwardTrendLine:
            del point

    def clearDownwardTrendLine(self):
        for point in self.downwardTrendLine:
            del point

    # Use Least Square Method to determine whether trending upward or downward
    def WhatIsTrendDoing(rates):
        if (len(self.rsiRates) < 10):
            return "nothing"

        omega = Decimal(".0000005")
        delta = Decimal("-.0000005")

        # Look at last, say, 10 Data Points
        recentRates = self.rsiRates[-10:]
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

        if slope > omega:
            return "advancing"
        elif slope < delta:
            return "retreating"
        else:
            return "nothing"
