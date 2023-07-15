from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from   inspect import currentframe, getframeinfo
from   time import sleep
import threading
import os

import sys


os.chdir("..")
print(os.getcwd())
print(os.listdir())
print("-----")

#TODO fix this
sys.path.append('/home/garrett/Documents/NoGambleNoFuture/May_Bot_2023/May_Bot_2023_Currency_trading/')
sys.path.append('/home/garrett/Documents/NoGambleNoFuture/May_Bot_2023/May_Bot_2023_Currency_trading/API_calls')
print(sys.path)
from API_calls.Kucoin.Kucoin___ import *






#Main.py -> start thread to Run Bot -> Which runs in a timer loop that just track time, then spins off thread to call data if timer goes off for a specifc task



#hmmm what should this do
#For now I just want to get an orderbook printing on the screen


#Call APIs
#If success call to update Pandas
#THis could be  a good expeirment with threading, parrell, async in python and in general
#So data bot is going to just call the API on timers
#

#


def runTimers(
        timer_for_data = 
            {'orderbook_Onada': 
             {'checkTimer' : (10, None), 
              'currenCs': ["ETHUSDTM",  "XBTUSDTM", "ADAUSDTM", "DOTUSDTM","LTCUSDTM"], 
              'datafunction': get_orderbook_kucoin} }):



    while True:
        for _, dict_of_data_feeds in timer_for_data.items():
            (limit_time, last_pulled_time) = dict_of_data_feeds['checkTimer']
            now  = datetime.now()
            #Only happens on the first call ever

            

            if last_pulled_time == None: 
                print("firstInit timer")
                #call data
                #so success check/error handling should go here
                dict_of_data_feeds['checkTimer'] = (limit_time, datetime.now())
            else:

                time_delta_int = int((now - last_pulled_time).total_seconds())

                print(time_delta_int >= limit_time, "now", now,  "last_pulled_time", last_pulled_time, "limit_time", limit_time)
                if time_delta_int >= limit_time:
                    print("yeah")
                    #call data
                    square_thread = threading.Thread(target=botLogic, args=(dict_of_data_feeds['datafunction'],  print, dict_of_data_feeds['currenCs']))
                    square_thread.start()
                    
                    #so success check/error handling should go here
                    dict_of_data_feeds['checkTimer'] = (limit_time, datetime.now())



        sleep(1)


def botLogic(func,  toCall, *funcArgs):
    
    
    res = func(*funcArgs)
    #TODO check for success instead of just straight passing
    toCall(res)
    print("success to callback")




runTimers().start()