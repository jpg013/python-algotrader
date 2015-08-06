from decimal import *
getcontext().prec = 7

# Formula for the Parabolic Sar is
# SAR_next = SAR_current + AF * (EP - SAR_current)
# Acceleration factor starts at 0.02, increments by 0.02 every time new extreme point is achieved (caps at 0.20)
# When the price crosses the SAR then the position should be exited.
# We need an initial position

class ParabolicSAR():
    def __init__(self):
        self.period = []
        self.currentSAR = None
        self.extremePoint = Decimal('0')
        self.AF = Decimal('0.02')

    def run(self, rate):
        self.period.append(rate)
        if currentSAR is None:
            if (len(self.period) > 9):
                self.extremePoint = max(self.period, key=lambda rate: rate.highMid)
                self.currentSAR = min(self.period, key=lambda rate: rate.lowMid)
                self.period = []
        else:
            if rate.highMid > self.extremePoint:
                if self.AF < Decimal('0.20'):
                    self.AF += Decimal('0.02')
            nextSar = self.currentSar + self.AF * (self.extremePoint - self.currentSAR)
