
from time import sleep
from datetime import datetime, timedelta
#TODO I should make it so I get all my own time stamops
#along with the time stamps from the from the servers I am calling
#Logging purposes


import json
import os
from   urllib.error import HTTPError
import requests

def getCandles_fromOanada(currency, count = "3", bearerToken = None, accountNum = None):
    try:
        r = requests.get('https://api-fxtrade.oanda.com/v3/instruments/'+currency +'/candles?count='+ str(count) +'&price=M&granularity=M15',
            headers= { 'Content-Type': 'application/json','Authorization': 'Bearer ' + bearerToken}
            )
        r.raise_for_status()
        return (r.json(), True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
    except Exception as err:
        print(f'Other error occurred  in function getCandles_fromOanada: {err}')
    return ("", False)


def get_orderbook_from_Oanada(currency, bearerToken = None, accountNum = None):
    try:
        r = requests.get('https://api-fxtrade.oanda.com/v3/instruments/'+currency +'/orderBook',
            headers= { 'Content-Type': 'application/json','Authorization': 'Bearer ' + bearerToken}
            )
        r.raise_for_status()
        return (r.json(), True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
    except Exception as err:
        print(f'Other error occurred  in function getCandles_fromOanada: {err}')
    return ("", False)