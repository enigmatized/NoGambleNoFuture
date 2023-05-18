from datetime import datetime, timedelta, time
from   collections import defaultdict
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from   inspect import currentframe, getframeinfo
import requests
from   time import sleep
import os
import sys
import re


def printResults(isDebug, index____ , strategies):
        totalMoneyMade = 0
        (y______, x_____) = (list((strategies[strategy_name]["pandas_df"]).values())[0]).shape
        if isDebug:  print("x at the end pof the file", x_____)
        if index____ >=  (y______ -1) :
          for strategy_name, v in strategies.items():
            #print(" list of trades I should have made",  strategy_name, strategies[strategy_name]["log_trades_I_decided_to_make"])
            #print(" list of trades I should have exited", strategy_name, strategies[strategy_name]["list_of_results_from_orders_this_is_test"][-1])
            #print(" list of trades I should have exited", strategy_name, strategies[strategy_name]["list_of_final_stats"][-1])
            
            
            for finalResults_ in strategies[strategy_name]["list_of_final_stats"] :
              for finalResults in finalResults_:
                print("finalResults--------->", finalResults)
                (result_from_exit, info_before_that) = finalResults

                #SO I am pretty mixed up here, why do I get a dict here?
                #How am I suppose to know if the intent of the trade was long? green.
                

                print("\n----result_from_exit ----", result_from_exit)
                print("\n----info_before_that ----", info_before_that)
                # print("\n----info_before_that ----", type(info_before_that))
                # print("\n----info_before_that 0 ----", info_before_that[0]['price_our_decision_algo_decided_to_exit_trade'])
                # print("\n----info_before_that 1 ----", info_before_that[1]['price_decsion_to_make_trade_was_based_on'])
                value_I_exited = result_from_exit['price_our_decision_algo_decided_to_exit_trade']
                value_I_entered = info_before_that['price_decsion_to_make_trade_was_based_on']
                profit = (value_I_exited- value_I_entered) if info_before_that['direction'] == "green" else value_I_entered -  value_I_exited 
                totalMoneyMade+=profit
                print("!!!!!!!!!!!!! profit:", profit )
                print()

          #TODO this is where I calculate the results from back Testing
          
          sys.exit("Total Profit: " + str(totalMoneyMade) )