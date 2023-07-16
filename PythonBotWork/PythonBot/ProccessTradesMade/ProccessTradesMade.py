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



#Should take a <dict time [<stats, info>]>  -- for orders_made
#SHould take a current trades in
#Should return a dictionary of updated current_Trades_in
def proccess_orders_made_return_trades_in(
          orders_made, 
          current_trade_in,
          proccessOrdersDebug = False
          ):

    for time_, dict_of_list_of_dict_of_orderes_stats in  orders_made.items():
        if proccessOrdersDebug: print("what is this", dict_of_list_of_dict_of_orderes_stats)
        for dict_response_from_order_made in dict_of_list_of_dict_of_orderes_stats["curr_orders_after_made"]:
            if proccessOrdersDebug : print("dict_of_list_of_dict_of_orderes_stats", dict_of_list_of_dict_of_orderes_stats)
            wasASuccess = dict_response_from_order_made["wasASuccesfulOrder"]
            currenC     = dict_response_from_order_made["currency____"]
            amount      = dict_response_from_order_made["amout_I_beleive?"]
            if wasASuccess:
                current_trade_in[time_][currenC].append(dict_response_from_order_made)
            else:
                print("WHAT THE FUCK ORDER DIDNT go through on", currenC, "for time", time_ )
    return current_trade_in

def proccess_exits_made_return_trades_in(orders_made,
                                         current_trade_in,
                                         debugPrints = False):
    #TODO improve this, so it can be 
    # calulcated and make stats on it
    #trades_exit = defaultdict(list)
    stats_tracking_ls = []



    if debugPrints: print("orders_made_what_is_this", orders_made)
    if debugPrints: 
        print("\n-----------\n")
        print("current_trade_in keys", current_trade_in.keys())
        print("current_trade_in looking up 240min", current_trade_in['240min'])
    for notSureTheKey_time, another_defult_dict  in  orders_made.items():
        for cuurenC, list_of_order_excuted in another_defult_dict.items():
             for order_excuted in list_of_order_excuted:
                wasASuccess =order_excuted["wasSucces"]
                if wasASuccess:
                        #addOrMinus = 1 if dirrection == "green" else -1
                        # current_trade_in[time_][currency_] += addOrMinus
                        if debugPrints: print("notSureTheKey_time", notSureTheKey_time)
                        
                        #TODO logic will have to be added to there be multi amount of trades 
                        value = current_trade_in[notSureTheKey_time][cuurenC].pop()
                        #TODO this should throw an error if the list is zero to beging with
                        #ACTAUALLLY this should never happen unless logic above stream is not working
                        #Because this is saying I exited an order
                        #That 
                        #print("WHAT THE FUCK IS VALUE", value)
                        stats_tracking_ls.append( (order_excuted,  value) )
                else:
                        print("WHAT THE FUCK ORDER DIDNT go through on", cuurenC, "for time", notSureTheKey_time )
        


    return (current_trade_in, stats_tracking_ls)

