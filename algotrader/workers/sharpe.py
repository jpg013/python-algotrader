import datetime
import numpy
import math
import requests
requests.packages.urllib3.disable_warnings()


class SharpeProcessor():
    def __init__(self):
        pass

    def getDailyReturns(self, rates):
        dailyReturns = []
        for idx, val in enumerate(rates):
            if idx == 0:
                continue
            else:
                rate = rates[idx]
                prevRate = rates[idx-1]
                dailyReturn = (rate["adjClose"] - prevRate["adjClose"]) / prevRate["adjClose"]
                dailyReturns.append(dailyReturn)
        return dailyReturns

    def computeLongSharpe(self, dailyReturns):
        # Compute Daily Return
        excessReturns = []
        for dailyReturn in dailyReturns:
            excessDailyReturn = dailyReturn - (float("0.04") / float("252"))
            excessReturns.append(excessDailyReturn)

        avg = getAverage(excessReturns)
        sharpeRatio = math.sqrt(252) * avg / numpy.std(excessReturns)
        return sharpeRatio

    def computeLongShortMarketNeutralSharpe(self, longRates, shortRates):
        assert len(longRates) == len(shortRates)

        longDailyReturns = []
        shortDailyReturns = []
        for idx, val in enumerate(longRates):
            if idx == 0:
                continue
            else:
                longRate = longRates[idx]
                shortRate = shortRates[idx]
                prevLongRate = longRates[idx-1]
                prevShortRate = shortRates[idx-1]

                longDailyRet = (longRate["adjClose"] - prevLongRate["adjClose"]) / prevLongRate["adjClose"]
                shortDailyRet = (shortRate["adjClose"] - prevShortRate["adjClose"]) / prevShortRate["adjClose"]

                longDailyReturns.append(longDailyRet)
                shortDailyReturns.append(shortDailyRet)

        assert len(longDailyReturns) == len(shortDailyReturns)
        netDaily = []

        for idx, val in enumerate(longDailyReturns):
            longRet = longDailyReturns[idx]
            shortRet = shortDailyReturns[idx]

            netRet = (longRet - shortRet) / 2
            netDaily.append(netRet)

        avg = getAverage(netDaily)
        sharpeRatio = math.sqrt(252) * avg / numpy.std(netDaily)
        return sharpeRatio

    def computeMaxDrawdown(self, longRates, shortRates):
        longReturns = self.getDailyReturns(longRates)
        shortReturns = self.getDailyReturns(shortRates)
        netReturns = getHedgedNetReturns(longReturns, shortReturns)

        cumulativeCompoundedReturns = []
        for idx, val in enumerate(netReturns):
            netReturn = netReturns[idx]
            if idx == 0:
                cumulativeCompoundedReturns.append(netReturn)
                continue
            else:
                prevCumRet = cumulativeCompoundedReturns[idx-1]
                val = (1+prevCumRet) * (1+netReturn) - 1
                cumulativeCompoundedReturns.append(val)

        highWatermarks = []
        for idx, val in enumerate(cumulativeCompoundedReturns):
            cumRet = cumulativeCompoundedReturns[idx]
            if idx == 0:
                highWatermarks.append(cumRet)
            else:
                val = max(cumRet, highWatermarks[idx-1])
                highWatermarks.append(val)

        assert len(cumulativeCompoundedReturns) == len(highWatermarks)
        drawdowns = []

        for idx, val in enumerate(cumulativeCompoundedReturns):
            cumRet  = cumulativeCompoundedReturns[idx]
            highWatermark = highWatermarks[idx]
            val = (1 + cumRet) / (1 + highWatermark) - 1
            drawdowns.append(val)

        drawdownLengths = []
        for idx, val in enumerate(drawdowns):
            drawdown = drawdowns[idx]
            if idx == 0:
                if drawdown < float(0.0):
                    drawdownLengths.append(1)
                else:
                    drawdownLengths.append(0)
            else:
                if drawdown < float(0.0):
                    prevDrawdown = drawdownLengths[idx-1]
                    val = prevDrawdown + 1
                    drawdownLengths.append(val)
                else:
                    drawdownLengths.append(0)

        maxDrawdown = max(drawdownLengths)

def getHedgedNetReturns(longReturns, shortReturns):
    assert len(longReturns) == len(shortReturns)
    netDaily = []
    for idx, val in enumerate(longReturns):
        longRet = longReturns[idx]
        shortRet = shortReturns[idx]

        netRet = (longRet - shortRet) / 2
        netDaily.append(netRet)
    return netDaily

def getAverage(s):
    return sum(s) * float("1.0") / len(s)
