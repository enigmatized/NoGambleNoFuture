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



def createStateMap(json_currency_to_optimized_values):

  #print(stateMap) #Debug Print
  dict_currency_to_stateMap = defaultdict(list)
  #print(json_currency_to_optimized_values.keys())
  for currency, stateMap in json_currency_to_optimized_values.items():
    #Create state map for multiple time frames
    # print("Before", json_currency_to_optimized_values.keys())
    for k, v in stateMap.items():
      # print(currency, "currency\n", k, " in createStateMap\n", v)
      stateMap[k] = {'count'      : 0, 
                    'last'        : None, 
                    'lastColorBar': "green",
                    'typeOfPurchase' : None, # change this to be able to make multiple orders in one buy time
                    'tracker'     : [], 
                    'profit'      : 0, 
                    'buys'        : [] , 
                    'shorts'      : [],
                    'pricePurchased' : 0,  
                    'inTrade'     : False, 
                    'enoughData'  : False,
                    #'timesToCheckForTrade' : v,
                    'timesToCheckForTrade' : v[0],
                    'optimizedValues' : v[1],
                    'Heikin-Ashi' : True,
                    'trades_to_make' : [],
                    'curr_trades_on' : [],
                     'curr_orders_after_made'   : [],
                     'exit_trade_singal': [],
                     'trades_exited_attempt' :[],
                     'successful_exited_trades' :[]
                    }
    
    dict_currency_to_stateMap[currency] = stateMap
  return dict_currency_to_stateMap

def make_current_state(mainDf, stateMap ):
  for index, row in mainDf.iterrows():
      for k, v in stateMap.items(): 
        # This will need to be changed in the future 
        #so that if I am trading on the 4hr, 
        #and on the 15min things are looking bad, 
        #to be able to get out of the trade
        if str(row['time']) in  v['timesToCheckForTrade'] :
          #print(k, row['timeOnly'] ) #This seems to show that the above if #statement is working properly
                                      #Maybe in the future a unit test on this 

          bar_candles_or_heikin_ankiki =  ('heikin_ashi_open', 'heikin_ashi_close') if True else ('open', 'close') #Change this in the future
          #State Variables for the current state


          cur       = "green" if row[bar_candles_or_heikin_ankiki[1]] >= row[bar_candles_or_heikin_ankiki[0]] else "red"
          lastCount = stateMap[k]["count"]
          countCur = 0 if stateMap[k]["lastColorBar"] != cur else   (stateMap[k]['count'] + 1)
          curCount  = stateMap[k]["count"] + 1 if stateMap[k]["lastColorBar"] == cur else 0
          stateMap[k]["lastColorBar"] =  cur
          stateMap[k]["tracker"].append( (stateMap[k]["lastColorBar"] ,
                                      countCur))
          stateMap[k]["count"] = countCur
  
  return stateMap