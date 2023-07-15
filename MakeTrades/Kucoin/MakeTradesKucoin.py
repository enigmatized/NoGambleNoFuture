from collections import defaultdict
import requests
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime, timedelta, time
from inspect import currentframe, getframeinfo
import loggging

os.chdir("../../../kucoin_futures_python_sdk/")
print(os.getcwd())



def make_orders_for_correlated_movers_only_strategy(
      logger_,
      isCsv,
      decideToMakeTrade,
      trades_to_make_dict, 
      secret_api_info,
      isLiveTrading
      ):
  
  if not decideToMakeTrade: return ({}, ) #Why is this here?
  
  tradesMade  = defaultdict(dict)
  for time, dict_of_lists_of_trades_to_make in trades_to_make_dict.items():
    #TODO this ifstatement seems hacky, might want to remove this later
    if 'trades_to_enter_singal' in dict_of_lists_of_trades_to_make.keys() and len(dict_of_lists_of_trades_to_make['trades_to_enter_singal']) >0 : 

      logger_.info("In  make_orders_for_correlated_movers_only_strategy, should be making a trade")
      oanada_response_to_orders = []

      for (dirrection, currency__,  amount, curPrice_, myTime, unixTime, timeStamp ) in dict_of_lists_of_trades_to_make['trades_to_enter_singal']:  
        if isCsv:
        # How do I check if this has been a success?
          (a,b) = (True , True)#TODO make this a json response of the price excuted
        else:
          (a,b)= make_market_kucoin( # returns -> (r.json(), True)
            dirrection, 
            currency__, 
            amount,
            bearerOanada,
            accountNumOanda
            )
        print("WHAT THE FUCK IS DIRECTION", dirrection, "dirrection == green", dirrection == "green")
        amountToKnowLater = 1 if dirrection == "green" else -1 #This is always returning a -1, which is weird?
        buy_or_sell = "buy" if dirrection == "green" else "sell"
        #So there might be two things are happennig
        #That we are updating the statemap more often then I realize?
        #Because we shouldn't be getting here that often
        #Also wtf is direction?!
        logging_result_from_trade_made= {
                      'json_response_if_api_call': a,
                      'wasASuccesfulOrder': b,
                      'currency____' : currency__,
                      'amout_I_beleive?' : amountToKnowLater,
                      'direction': dirrection,
                      'long/short': dirrection,
                      'price_decsion_to_make_trade_was_based_on': curPrice_,
                      'myTime_decsion_to_make_trade_was_based_on': myTime,
                      'unixTime_decsion_to_make_trade_was_based_on': unixTime,
                      'timeStampFromDecisionToMakeTrade' : timeStamp,
                      }
        oanada_response_to_orders.append( logging_result_from_trade_made) 

      #TODO only do this if there was an success
      #This assumes if all the trades go through successfully
      tradesMade[time]['curr_orders_after_made']   = oanada_response_to_orders
      
      #I am not sure if this fucked up logic works?
      # I get the point, I want to clear trades to make 
      # This is for live trading, just in case a trade doesn't go through
      # I think this is a major TODO 
      dict_of_lists_of_trades_to_make['trades_to_enter_singal'] = [] 
      trades_to_make_dict[time] = dict_of_lists_of_trades_to_make 


  return (tradesMade, trades_to_make_dict)






def make_market_kucoin(
      dirrection,
      currency = "EUR_USD", 
      amount = "1", 
      bearerTokenOanda = None, 
      accountNumOanda = None
      ):



    print("about to place an order", "direction:", dirrection, "currency", currency, "amount", amount)
       
    units         = "1" if dirrection == "green" else "-1"
    data = {"order": {
            "units": units,
            "instrument": currency,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
            }}
    try:
        r = requests.post('https://api-fxtrade.oanda.com/v3/accounts/'+accountNumOanda+'/orders',
            headers = { 'Content-Type': 'application/json','Authorization': 'Bearer '+ bearerTokenOanda}, #Correct this to be read from file
            json    = data,
            )
        r.raise_for_status()
        what_is_this = (r.json(), True)
        print(what_is_this)
        return (r.json(), True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
        print(price, optmizedStopLossValue, dirrection, currency)
    except Exception as err:
        print(f'Other error occurred, make_market_orders_for_correlated_assets: {err}')
    return ("", False)
















#THIS is old
#TODO throw away

def make_orders_(price, optmizedStopLossValue, dirrection, currency = "EUR_USD", amount = "1"): #TODO make this function take arguements for different instruments
                   #TODO function defintion of return type
                   #Put all these functions in seperate file/folder 
    # for k, v in currTades.items():'
    print(price, optmizedStopLossValue, dirrection, currency)
    units         = "1" if dirrection == "green" else "-1"
    #stopLossValue = price - optmizedStopLossValue if dirrection == "green" else price + optmizedStopLossValue
    stopLossValue = price - 0.005 if dirrection == "green" else price + 0.005
    if True:

        # data  =  { 
        #     "order": {
        #       "price": "1.9700", #Todo Make this a limit order so it is optimized
        #       "units": str(units),
        #       "instrument": currency,
        #       "timeInForce": "GTC",
        #       "type": "MARKET",
        #       "positionFill": "DEFAULT",
        #       "stopLossOnFill": {
        #         "timeInForce": "GTC",
        #         "price": str(stopLossValue)
        #           },
        #       }
        #      }
        
        data = {"order": {
    "units": "1",
    "instrument": "EUR_USD",
    "timeInForce": "FOK",
    "type": "MARKET",
    "positionFill": "DEFAULT",
    "stopLossOnFill": {
                 "timeInForce": "GTC",
                 "price": str(stopLossValue)
                   }
  }}
    try:
        print("Enter the trade !!!!!!!!!!!!!!!!!!!!!!!", dirrection, price, stopLossValue, units)
        r = requests.post('https://api-fxtrade.oanda.com/v3/accounts/'+accountNumOanda+'/orders',
            headers = { 'Content-Type': 'application/json','Authorization': 'Bearer '+ bearerTokenOanda}, #Correct this to be read from file
            json    = data,
            )
        r.raise_for_status()
        what_is_this = (r.json(), True)
        print(what_is_this)
        return (r.json(), True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
        print(price, optmizedStopLossValue, dirrection, currency)
    except Exception as err:
        print(f'Other error occurred in make_orders_: {err}')
    return ("", False)