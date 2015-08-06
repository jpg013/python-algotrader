from .api_config import *
from .api_rates import *
import math
import time
import threading
lock = threading.Lock()
is_dst = time.daylight and time.localtime().tm_isdst > 0
utc_offset = (time.altzone if is_dst else time.timezone)

class OandaApi:
    def __init__(self, rateQueue):
        self.configuration = configurationSettings["fxPractice"]
        self.configuration['instrument'] = instrument
        self.configuration['granularity'] = granularity
        self.configuration['period'] = period
        self.configuration['headers'] = {'Authorization' : 'Bearer ' + self.configuration['accessToken']}
        self.rateQueue = rateQueue

    def getHistoricalRates(self):
        candlewidth = GetGranularitySeconds(self.configuration['granularity'])
        response = getInstrumentHistory(self.configuration)
        # Request Instrument Rate
        candles = json.loads(response.decode())['candles']
        print(candles)
        while True:
            pass
        #return candles

    def getRatesInDateRange(self, start, end):
        candlewidth = GetGranularitySeconds(self.configuration['granularity'])
        response = GetDateRangeHistory(self.configuration, start, end)
        # Request Instrument Rate
        candles = json.loads(response.decode())['candles']
        print(candles)
        return candles

    def streamRates(self):
        streamObj = {'hasChanges' : False, 'data' : None}
        emitThread = threading.Thread(target=emitStreamData, args=(streamObj, self.rateQueue, GetGranularitySeconds(self.configuration['granularity'])))
        emitThread.daemon = False
        emitThread.start()
        response = streamInstrumentRates(self.configuration)
        if response.status_code != 200:
            print(response.text)
        for line in response.iter_lines():
            if line:
                tick = parseTick(line)
                if tick:
                    lock.acquire()
                    streamObj['data']= tick
                    streamObj['hasChanges'] = True
                    lock.release()

### Static Methods ###
def GetGranularitySeconds(granularity):
    if granularity[0] == 'S':
        return int(granularity[1:])
    elif granularity[0] == 'M' and len(granularity) > 1:
        return 60*int(granularity[1:])
    elif granularity[0] == 'H':
        return 60*60*int(granularity[1:])
    elif granularity[0] == 'D':
        return 60*60*24
    elif granularity[0] == 'W':
        return 60*60*24*7
    #Does not take into account actual month length
    elif granularity[0] == 'M':
        return 60*60*24*30

def emitStreamData(streamObj, rateQueue, candlewidth):
    while True:
        lock.acquire()
        if (streamObj['hasChanges']):
            rateQueue.put(streamObj['data'])
            streamObj['hasChanges'] = False
        else:
            data = streamObj['data']
            if data:
                data['time'] = math.trunc(time.time() + utc_offset)
                rateQueue.put(data)
        lock.release()
        time.sleep(candlewidth)

def parseTick(data):
    jsonBlob = json.loads(data.decode('utf-8'))
    if "tick" in jsonBlob:
        tick = jsonBlob["tick"]
        tick["time"] = time.mktime(time.strptime(str(tick['time']),  '%Y-%m-%dT%H:%M:%S.%fZ'))
        if "ask" in tick and "bid" in tick: # Set the price as midpoint
            price = (float(tick["ask"]) + float(tick["bid"])) / 2
            tick["price"] = price
            return tick



#http://api-sandbox.oanda.com/v1/candles?instrument=EUR_USD&granularity=M1&start=2015-03-02T00%3A00%3A00Z&end=2015-03-02T01%3A59%3A59Z&candleFormat=bidask
