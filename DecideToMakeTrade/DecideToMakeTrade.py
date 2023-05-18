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



#This should return a tuple with
#  a dictionary for trades to enter/exit
#  And a Bool
#  

#hmmm, I like the above?
#But I am wondering what is actually the best way to do this
#Because I imagine a future
#Where the trading signal is also based on a "risk manager algo"
#Where they might work together
#I think for now, similiar to above is okay?
#Maybe I am wondering if each strategy should have a stateMap for trades.
#I actuall think that is a more ideal idea

#Note for this trading strategy the stateMap looks like
##stateMap Dict<time, Dict<Currency, Innder_state_map >>
#ANd I want the signal to be accross all pairs
#So 
def deciding_to_make_trades_based_on_updated_stateMap_correlated_moves_only(
      cur_state_map, 
      list_of_time_frames_to_trade_on,
      isDebug = False,
      isLiveTrading = False,
      ):
  
  decidedToMakeTrade = False #Return this to save time down the road
  exitSignal         = False

  result_keyTime_valueDictOfTrades = defaultdict(dict)
  
  for time, dict_of_CurrenC_and_innerStateMap  in cur_state_map.items():
    #TODO THIS IS A SHITTY HACK TO GET ONE TIME FRAME 
    #print("NOTE SURE IF THIS WILL WORK, time in list_of_time_frames_to_trade_on: ", time in list_of_time_frames_to_trade_on, "time", time, "list_of_times", list_of_time_frames_to_trade_on)
    if time in list_of_time_frames_to_trade_on:
      d = {"trades_to_enter_singal": [],
          "exit_trade_singal" : [],
          }
      trades_to_make = []
      count = 0 #If count goes past threshold, get in trade
                #Oh I should optimize it for those currencies as well
      if isDebug:
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno,
                  "\n\tlist_of_time_frames_to_trade_on", 
                  list_of_time_frames_to_trade_on,
                  "\n\tkeys of dict_of_CurrenC_and_innerStateMap",
                    dict_of_CurrenC_and_innerStateMap.keys()
                  )

      for currenC, innerStateMap in dict_of_CurrenC_and_innerStateMap.items():
          if isDebug:
              frameinfo = getframeinfo(currentframe())
              print(frameinfo.filename, frameinfo.lineno,
                    "time", time, 
                    "currenC",  currenC , "innerStateMap", innerStateMap )
        
        #if len(innerStateMap["tracker"]) >1: #THIS SHOULD NEVER BE AN ISSUE! This should throw error?
          (cur_color, cur_count, cur_price, cur_time_unix, cur_time_my)            = innerStateMap["tracker"][-1]
          (previous_color, previous_count, last_price, _ , _) = innerStateMap["tracker"][-2]
          if isDebug:
              frameinfo = getframeinfo(currentframe())
              print(frameinfo.filename, 
                    frameinfo.lineno,
                    currenC, 
                    "in deciding_to_make_trades_based_on_updated_stateMap\n\t current ", 
                    (cur_color, cur_count),
                    currenC, 
                    "in deciding_to_make_trades_based_on_updated_stateMap\n\t previous ", 
                    (previous_color, previous_count))
          
          #TODO #This is supposed to be decided on optimized values. Will improve later
          if previous_count == 0 and cur_color == previous_color:
              count +=1
              trades_to_make.append((cur_color, currenC, 1, cur_price, cur_time_unix, cur_time_my, datetime.now()))

          elif cur_count == 0 :
            exitSignal = True
            #TODO #This isn't optmized to exit trades based on stop loss optimized value 
            d["exit_trade_singal"].append(
               (cur_color, 
                currenC, 1, 
                cur_price, 
                cur_time_unix, cur_time_my, datetime.now()))
      
      if count >= 3: 
          d['trades_to_enter_singal']=  trades_to_make #TODO update this arguement through optimized values
          decidedToMakeTrade =True
          if isLiveTrading: print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Should be entering a trade!!!!!!!!")
      result_keyTime_valueDictOfTrades[time] = d
    
  return (result_keyTime_valueDictOfTrades, decidedToMakeTrade, exitSignal)
