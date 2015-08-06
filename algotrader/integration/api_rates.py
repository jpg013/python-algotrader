import urllib.request
from urllib.parse import urlparse
import urllib
import requests
requests.packages.urllib3.disable_warnings()
import json

def getInstrumentPrice(config):
    url = config['domain'] + ''.join(["/v1/prices?instruments=", config['instrument']])
    req = urllib.request.Request(url, headers = config['headers'])
    resp = urllib.request.urlopen(req)
    rawData = resp.read()
    return rawData

def getInstrumentHistory(config):
    url = config['domain'] + ''.join(["/v1/candles?start=2015-03-03T00%3A00%3A00&end=2015-03-04T00%3A00%3A00&instrument=", config['instrument'], "&granularity=M1&candleFormat=bidask"])
    print(url)
    req = urllib.request.Request(url, headers = config['headers'])
    resp = urllib.request.urlopen(req)
    rawData = resp.read()
    return rawData

def GetDateRangeHistory(config, start, end):
    startUrl = urllib.parse.quote(start)
    endUrl = urllib.parse.quote(end)
    url = config['domain'] + ''.join(["/v1/candles?start=", startUrl, "&end=", endUrl, "&instrument=", config['instrument'], "&granularity=M1&candleFormat=bidask"])
    req = urllib.request.Request(url, headers = config['headers'])
    resp = urllib.request.urlopen(req)
    rawData = resp.read()
    return rawData


#def getInstrumentDateHistory(config, start, end)

def streamInstrumentRates(config):
    s = requests.Session()
    url = "https://" + config['streamDomain'] + "/v1/prices"
    headers = config['headers']
    params = {'instruments' : config['instrument'], 'accountId' : config['accountId']}
    req = requests.Request('GET', url, headers = headers, params = params)
    pre = req.prepare()
    response = s.send(pre, stream = True, verify = False)
    return response
