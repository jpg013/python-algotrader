from decimal import *
getcontext().prec = 7

class RsiIndicator():
    def __init__(self):
        self.rsiLimit = 15
        self.rsiRates = []

    def run(self, rate):
        self.rsiRates.append(rate)
        if (len(self.rsiRates) < (self.rsiLimit)):
            return
        self.pruneRsiRates()
        self.computeRSI(rate)

    def computeRSI(self, rate):
        index = 0
        emaSumGain = Decimal('0')
        emaSumLoss = Decimal('0')
        sumGain = Decimal('0')
        sumLoss = Decimal('0')
        for rsiRate in self.rsiRates:
            if index == 0:
                index += 1
                continue
            else:
                prevRate = self.rsiRates[index-1]
                index += 1
                currEMAIndex = rsiRate.getMovingAverageVal('ema')
                prevEMAIndex = prevRate.getMovingAverageVal('ema')
                currIndex = rsiRate.closeMid
                prevIndex = prevRate.closeMid

                if currEMAIndex > prevEMAIndex:
                    emaSumGain += (currEMAIndex - prevEMAIndex)
                elif currEMAIndex < prevEMAIndex:
                    emaSumLoss += (prevEMAIndex - currEMAIndex)

                if currIndex > prevIndex:
                    sumGain += (currIndex - prevIndex)
                elif currIndex < prevIndex:
                    sumLoss += (prevIndex - currIndex)

        avgEmaGain = emaSumGain / Decimal(str(self.rsiLimit-1))
        avgEmaLoss = emaSumLoss / Decimal(str(self.rsiLimit-1))
        avgGain = sumGain / Decimal(str(self.rsiLimit-1))
        avgLoss = sumLoss / Decimal(str(self.rsiLimit-1))

        if avgLoss == Decimal('0'):
            rs = Decimal('100')
        else:
            rs = avgGain / avgLoss

        if avgEmaLoss == Decimal('0'):
            emaRs = Decimal('100')
        else:
            emaRs = avgEmaGain / avgEmaLoss

        rsi = Decimal('100') - (Decimal('100') / ((Decimal('1') + rs)))
        emaRsi = Decimal('100') - (Decimal('100') / ((Decimal('1') + emaRs)))

        rate.setRsi(rsi)
        rate.setEmaRsi(emaRsi)

    def pruneRsiRates(self):
        while(len(self.rsiRates) > self.rsiLimit):
            rate = self.rsiRates.pop(0)
            del rate
