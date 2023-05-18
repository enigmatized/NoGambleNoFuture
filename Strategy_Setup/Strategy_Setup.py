from datetime import datetime, timedelta, time


from   collections import defaultdict
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from   time import sleep

import os
import sys
import re
###
## Import my local files
from Account_Info_Setup import *


from Step1InitDf.InitDf_only_correlated_trade_at_once import *


from API_calls import *
from InitStateMap.InitStateMap_for_correlated_excution import *
from UpdatePandasDf.UpdatePandasDf_currencies_move_together import *
from UpdateStateMap.UpdateStateMap_correlated_move_only import *

from DecideToMakeTrade.DecideToMakeTrade   import *
from MakeTrades.MakeTrades                 import *
from ProccessTradesMade.ProccessTradesMade import *
from ExitTrades.ExitTrades                 import *



def makeStrategies():

    return {

      #TODO, I am realizing that a strategy should have a data source
      #This way you can have multiple strategies use the same data source
      #And also you can muliple data sources or exchange connections, running the same strategy 
    

        #TODO holly shit there is a lot to optimize with this strategy
        #1. The stop loss for each time frame
        #2. The take profit for each time frame
        #3. setting up a better proccess for make 3 purchases at once
        #   then exit out of 2 when I have made broken even, then let the winner run as long as I can
        #
        "henksi_3_currencies_move_together" : {
            "currencies_in_this_stratgey" : ["EUR_USD", "GBP_USD", "AUD_USD", "USD_CHF"],
            "times_frame_this_stratgey_is_focused_on": ["240min"], #4hour trades only
            #1. Init pandas df and statemap

            #This isn't the ttotally appropoate df for this
            #I am not sure if I should create its own
            #Or use a shared df
            #Because this could be a problem 
            #Actually I think a shared df would be wise for these two strategies
            #Otherwise I will have extra api calls
            "init_pandasDf"  : init_pandasDf_henksi_multiple_time_frames_but_trades_made_on_time_frame,
            "initStateMaps" : init_stateMap_for_only_correlatred_trades,
            #TODO make a test that ensures the state map is correctly made
            "check_if_state_map_init_correctly": None,
            "check_if_stateMap_is_correct_shape": check_if_stateMap_is_correct_shape, 


            #2.a Update pandas next iterOfPandas
               #function should take a if_a_test,
               #TODO index for backtesting with csv  file
            "get_new_pandas_info"     : get_new_pandas_info_update_pandas_df_henksi_3_currencies_move_together, #(isProd, isCsv, currnecies, currentPandasDf)  
            "check_if_new_pandas_info": check_if_new_pandas_info_for_correlated_trade_strat,


            #2.b Update next iter of stateMap State
            "update_state_map": update_state_map_from_new_pandas_info, #(dict_of_new_pandas_result, stateMap )


            #3. Logic to decide on making a trade
            "deciding_to_make_trade"   : deciding_to_make_trades_based_on_updated_stateMap_correlated_moves_only, #This should always return a (dict, bool)?
            #"trades_I_decided_to_make" : [], #TODO look into removing this, may not be needed
            "log_trades_I_decided_to_make" : [],
            "trades_to_make"       : defaultdict(dict),




            #TODO MANAGE RISK? Not sure how this should be involved?
            #4. Do what it needs to from that decision
            "make_orders" : make_orders_for_correlated_movers_only_strategy,



            #Proccess the results from making orders
            "proccess_orders_made" : proccess_orders_made_return_trades_in,
            #TODO make sure these time match what they are being looked up as
            "curr_trades_I_am_in" :  defaultdict(lambda: defaultdict(list)),
            
            # {
            #   "15min" : defaultdict(list),
            #   "30min" : defaultdict(list),
            #   "60min" : defaultdict(list),
            #   "240min":  defaultdict(list),
            #   }, #TODO unHardCodeThis/ time frame, that should come in the auto_
            
            "list_of_results_from_orders_this_is_test" : [],

            #This part will be majorly revised once risk management is involed
            "proccess_orders_to_exit": proccess_orders_to_exit_exit_trades_for_correlated_movements_only,

            "update_currOrders_from_exit_result" :  proccess_exits_made_return_trades_in,

            "list_of_final_stats" : [],


            #5. Track/manage trades
                #a. manuel stop losses
                #b. Basically stop loss? but what other risk management strategies should be involved?
                #c. Also there needs to be a meta risk management for strategies involved

            #TODO I think leaving the list of optimized values here might not be bad
            #Stop loss values
            #Limit order Values


        },
    }
