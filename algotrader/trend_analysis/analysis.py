# Definition for upward trend: 20 EMA slope is above zero and price action is greater than ema.
# Definition for downward trend: 20 EMA slope is below zero and price action is less than ema.
# Use Least Square Method

def TrendDirection(candles):
    xSum = Decimal('0') # Time Values
    ySum = Decimal('0') # CloseMid Values
    for candle in candles:
        xSum += Decimal(str(candle.time))
        ySum += rate.closeMid

    xBar = xSum / Decimal(str(len(recentRates)))
    yBar = ySum / Decimal(str(len(recentRates)))

    slopeNum = Decimal('0')
    slopeDen = Decimal('0')
    for rate in candles:
        x = Decimal(str(rate.time)) - xBar
        slopeNum += (x * (rate.closeMid - yBar))
        slopeDen += x ** 2

    slope = slopeNum / slopeDen

    lastCandle = candles[-1]

    if slope > Decimal('0') and (lastCandle.getMovingAverageVal("ema") > lastCandle.closeMid):
        return "upward"
    elif slope < Decimal('0') and (lastCandle.getMovingAverageVal("ema") < lastCandle.closeMid):
        return "downward"
    else:
        return "sideways"
