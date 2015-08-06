class Trend():
    def __init__(self, trendline, trendType, direction, maType, startRate):
        self.startRate = startRate
        self.trendLine = trendline
        self.trendType = trendType
        self.direction = direction
        self.movingAverageType = maType
        self.sortTrendLine()
        self.baseline = self.trendLine[-1]

    def addTrendRate(self, rate):
        self.trendLine.append(rate)
        self.sortTrendLine()

    def sortTrendLine(self):
        self.trendLine.sort(key=lambda x: getattr(x, "time"))

    def getSaveableObject(self):
        saveable = {}
        saveable['moving_average_type'] = self.movingAverageType
        saveable['direction'] = self.direction
        saveable['trend_type'] = self.trendType
        saveable['baselineId'] = self.baseline.id
        saveable['start_rate'] = self.startRate.id
        rateIds = []
        for rate in self.trendLine:
            rateIds.append(rate.id)
        saveable['trend_rates'] = rateIds
        return saveable
