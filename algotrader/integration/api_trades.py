import urllib.request
import urllib.parse

import requests
requests.packages.urllib3.disable_warnings()
import json

def getOpenTrades(config):
    url = config['domain'] + ''.join(["/v1/accounts/",config['accountId'], "/trades?instruments=", config['instrument']])
    req = urllib.request.Request(url, headers = config['headers'])
    resp = urllib.request.urlopen(req)
    rawData = resp.read()
    return rawData