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


""" THis is a statemap creaation for when only EUR_USD, GBP_USD and AUD_USD or all going in the same direction"""

#I AM NOT DOING this properly
#TODO My optimized values should have the currencies I am trading
#Right now I am just loading a random json that sorta works
#This will be something I need to work on
def createStateMap_for_only_correlatred_trades(json_currency_to_optimized_values, curruenciesToUse):

  #This should look like
  ##stratgey name
  ###TimeFrame
  ####StateMap


  #print(stateMap) #Debug Print
  dict_of_time_to_stateMaps = defaultdict(dict)
  #print(json_currency_to_optimized_values.keys())
  currencies = curruenciesToUse
  #currencies = json_currency_to_optimized_values.keys()

  for _, stateMap in json_currency_to_optimized_values.items():
    #Create state map for multiple time frames
    # print("Before", json_currency_to_optimized_values.keys())
    for k, v in stateMap.items():
      for currenC in currencies:
        # print(currency, "currency\n", k, " in createStateMap\n", v)
        dict_of_time_to_stateMaps[k][currenC] = {'count'      : 0, 
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

    #dict_of_time_to_stateMaps[k] = stateMap
  return dict_of_time_to_stateMaps


#TODO throw error
def check_if_stateMap_is_correct_shape(statemap__, currenC):
  lsOfTimes =  list(statemap__.keys())
    
  #TODO fill this out in a more correct manner
  if len(lsOfTimes) != 4:
    print("TIMES ARE OFF ERROR") 
    print(lsOfTimes)
  
  #List of currencies 
  lsCurrenCFromStateMap = list(statemap__[lsOfTimes[0]].keys())
  if (len(lsCurrenCFromStateMap) != len(currenC)) and (sorted(lsCurrenCFromStateMap) == sorted(currenC)) : 
      print("ERRRRR----> len(statemap__.keys()) len(lsCurrenCFromStateMap) != len(currenC) and (sorted(lsCurrenCFromStateMap) == (sorted(currenC))")
      print("\t Should be ",  currenC) 
      print("\t But found  ", statemap__) 

def init_stateMap_for_only_correlatred_trades(isCsv, isDebug, dict_of_currency_to_pandas_df_, curruenciesToUse):
    # Reading from json file
    with open('Strategy_Setup/timeMapAndOptimizedValuesV2.json', 'r') as openfile: optimizedValuesNew = json.load(openfile)
    
    dict_of_state_maps      = createStateMap_for_only_correlatred_trades(optimizedValuesNew, curruenciesToUse)          
    
    # for currency, statemp in dict_of_state_maps.items(): 
      
    #   if  currency in curruenciesToUse:
    #     if debugMode : 
    #       print(currency)#, dict_of_currency_to_pandas_df_)
    #       print("statemp", statemp)
    #       print( dict_of_currency_to_pandas_df_.keys())
    #       print("dict_of_currency_to_pandas_df_[currency]", dict_of_currency_to_pandas_df_[currency])
    #     dict_of_state_maps[currency] = make_current_state(dict_of_currency_to_pandas_df_[currency],  statemp)
    if isDebug: print("!!!!!!!!!-> in  init_stateMap_for_only_correlatred_trades \t ", dict_of_state_maps)
    return dict_of_state_maps


def update_state_map__for_only_correlatred_trades(pandas_df, stateMap_):
  keys_of_pandas_df_dict = pandas_df.keys()
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