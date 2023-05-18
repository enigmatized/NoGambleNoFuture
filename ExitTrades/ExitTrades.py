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


#So this should
#1. iterate through the trades to exit
#2. if I a trade and I have an exit signal
#3. take cation
#4. the result

#dictionary_of_trades_to_exit 
#trades_currently_in
#result --- 
def proccess_orders_to_exit_exit_trades_for_correlated_movements_only(
      isCsv,
      dictionary_of_trades_to_exit, #?
      trades_currently_in, #?
      bearer, 
      accountInto,
      debugMode = False):
  
  #What should this return if this does nothing?
  if debugMode : print("trades_currently_in keys", list(trades_currently_in.keys()) )

  if debugMode : print("!!!!!Args \t dictionary_of_trades_to_exit ", dictionary_of_trades_to_exit ,"\n\t trades_currently_in", trades_currently_in)
  result_from_actions_ = defaultdict(lambda : defaultdict(list))

  # this is dog shit logic
  if debugMode :  print("!!!!!!!!!!!!trades_currently_in", sum([len(v) for k, v in trades_currently_in.items() ]) )
  #if len(list(trades_currently_in.keys())) == 0 :
     
  if sum([len(v) for k, v in trades_currently_in.items() ]) == 0 : return defaultdict(lambda : defaultdict(list))
  
  for time_, dict_of_list_of_trades_to_enter_exit in dictionary_of_trades_to_exit.items():
    
    if debugMode: 
       if time_ in  list(trades_currently_in.keys()):
          print("OH SHIT WE MIGHT, SHOULD BE EXITING A TRADE")
          print("240min key in trades_currently_in, ", trades_currently_in["240min"])
    if debugMode :  print("What does this look like, probably should be updated, dict_of_list_of_trades_to_enter_exit",  dict_of_list_of_trades_to_enter_exit)
    
    #GET A LIST OF ALL EXIT SIGNALS FOR THIS TIME FRAME
    list_of_exit_trade_signals = dict_of_list_of_trades_to_enter_exit["exit_trade_singal"] 
    if debugMode :  print("list_of_exit_trade_signals", list_of_exit_trade_signals)

    #NOW MATCH IT WITH trades in,

    
    
    if len(list_of_exit_trade_signals) == 0: pass

    else: 
       #print("list_of_exit_trade_signals", list_of_exit_trade_signals)
       for (cur_color, currenC, amount, 
            price_,  
            date_time_coming_from_canldes_chart, 
            unixTime, 
            time_stamp) in list_of_exit_trade_signals:
        
        amount_in_trade = trades_currently_in[time_][currenC] #
        if debugMode :  print("amount_in_trade ----- ", amount_in_trade)
        if len(amount_in_trade) == 0: pass
        #TODO improve this logic because it should on exit trades based on amount
        else:
           if not isCsv: 
            #TODO I WILL NEED TO FIX THIS like it looks like csv
            (json_response, wasSucces)= exit_trades_(cur_color, currenC,  bearer, accountInto) 
            result_from_actions_[time_][currenC].append( (time_, json_response, wasSucces, currenC, cur_color) )
           elif isCsv:
              
              json_response = { "time_" : time_,
                               "json_response":  {isCsv: "True, should return somethines, this is suppose to be a json data"},
                              "wasSucces" :True,
                              "currenC" : currenC,
                              "price_our_decision_algo_decided_to_exit_trade" : price_,
                              "cur_color": cur_color,
                              "gTimeStamp": datetime.now() } 
              result_from_actions_[time_][currenC].append( json_response)
              # ( time_,
              #      {isCsv: "True, should return somethines, this is suppose to be a json data"},
              #      True, 
              #      currenC, 
              #      cur_color 
              #    )
              
  return (result_from_actions_)




def exit_trades_(dirrection, currency = "EUR_USD", bearerTokenOanda = None, accountNumOanda = None):
  units         = "1" if dirrection == "green" else "-1"
  data  =  { 
            "order": {
              "units": units,
              "instrument": currency,
              "timeInForce": "GTC",
              "type": "MARKET",
              "positionFill": "DEFAULT",
              }
             }
  try:
        print("Exit the trade", dirrection)
        r = requests.post('https://api-fxtrade.oanda.com/v3/accounts/'+accountNumOanda+'/orders',
            headers = { 'Content-Type': 'application/json','Authorization': 'Bearer '+ bearerTokenOanda}, #Correct this to be read from file
            json    = data,
            )
        r.raise_for_status()
        return (r.json(), True)
  except HTTPError as http_err:
      print(f'HTTP error occurred: {http_err}')
      print(http_err.response.text)
      print("FAILURE with ")
  except Exception as err:
      print(f'Other error occurred in exit_trades_: {err}')
  return ("", False)
