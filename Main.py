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

runningInGoogleColab = False

## Import my local files
if runningInGoogleColab == True:
  print(os.getcwd())
  os.chdir("NoGambleNoFuture")
  print(os.getcwd())

from Strategy_Setup.Strategy_Setup         import *
from Account_Info_Setup import *

from Step1InitDf.InitDf_only_correlated_trade_at_once import *


from Step12PrintOutResults.Step12PrintOutResults import printResults



from API_calls import *
from InitStateMap.InitStateMap_for_correlated_excution import *
from UpdatePandasDf.UpdatePandasDf_currencies_move_together import *
from UpdateStateMap.UpdateStateMap_correlated_move_only import *

from DecideToMakeTrade.DecideToMakeTrade   import *
from MakeTrades.MakeTrades                 import *
from ProccessTradesMade.ProccessTradesMade import *
from ExitTrades.ExitTrades                 import *






#Should pass these values around so it is easier to 
#Pass to a google colab
(bearerTokenOanda, accountNumOanda) = getBearAndAccount()

secretInfo = {"bearerTokenOanda" : bearerTokenOanda, "accountNumOanda": accountNumOanda }

index____               = 300


#TODO clean this up, I have too many arguements here
useAPI_for_data_and_make_trades_on_exchange_ = False
sanityCheck_only_print_a_few_loops           = [True, 0]

#Remove these two, you do not need both
makeRealMoneyTrades         = False
makeOrders                  = True     #What does this do?

useAPIsToPopulatePandasInfo        = True
productoinMode                     = True   #I should have three modes, 
                                            #1. Live trading, 
                                            # 2. demo-trades
                                            # 3. Csv file back test
                                            #The ultimate model would do back testing
                                            #Simulation modelling
isLiveTrading                      = productoinMode


debugMode                          = False
shouldSleepForDebugPurposes        = True #This just sleeps in certain places, Only in places in code if debugmode is on

isCsv                   = False

debugMode               = False
isDebug                 = debugMode


#TODO set this up so it can correctly import files and libraries more seemlessly
runningInANoteBook =    False

strategies  = makeStrategies()


def main():
    print("Holly shit there is a lot going on here.")
    print("There is a lot to improve here")
    print("Weekend....")


if __name__ == "__main__":
    main()


    #TODO Move the init logic outside here
    #I do not want to be looking at it
    """ This Section is setting up the StateMaps, and Pandas DF for each strategy/robot"""
    #  strategies[k]
    for strategy in strategies.keys():
      strategies[strategy]["pandas_df"] = strategies[strategy]["init_pandasDf"](
        productionMod = useAPIsToPopulatePandasInfo,
        isCsv         = isCsv,
        currencys_    = strategies[strategy]["currencies_in_this_stratgey"],
        secretInfo    = secretInfo
        )
      
      
      #initStateMaps -> 
      #init_stateMap_for_only_correlatred_trades -> 
      #    createStateMap_for_only_correlatred_trades . createStateMap_for_only_correlatred_trades
      strategies[strategy]["stateMap"]  = strategies[strategy]["initStateMaps"](
        isCsv,
        debugMode,
        strategies[strategy]["pandas_df"],
        strategies[strategy]["currencies_in_this_stratgey"]
        )
      
      #print(strategies[strategy]["pandas_df"])
      #Wwait  what exactly is the data structure of stateMap? for this strategy
      for i in  range(0, index____):
        (strategies[strategy]["stateMap"], _ )  = update_state_map_from_new_pandas_info(
          isDebug,
          isCsv,                                                                  
          strategies[strategy]["pandas_df"],
          strategies[strategy]["stateMap"],
          strategies[strategy]["currencies_in_this_stratgey"],
          i,
          False)
      

      if isDebug : #TODO abstract this out, I do not want to be seeing this here
        strategies[strategy]["check_if_stateMap_is_correct_shape"](
          strategies[strategy]["stateMap"] , 
          strategies[strategy]["currencies_in_this_stratgey"])
        print("DEBUG | below is stateMap of strategy --->", strategy) #prints something like here henksi_multiple_time_frames_but_trades_made_on_time_frame

        if strategies[strategy]["stateMap"] != None and strategy == "henksi_3_currencies_move_together" :
          for kk, vv in strategies[strategy]["stateMap"].items():
            print("\t Time ->", kk)
            for kkk, vvv in vv.items():
              print("\t\t -> Currency", kkk)
              for kkkk, vvvv in vvv.items():
                print("\t\t\t", kkkk, vvvv )

        if shouldSleepForDebugPurposes :  sleep(30)



        if strategies[strategy]["stateMap"] != None and strategy == "henksi_multiple_time_frames_but_trades_made_on_time_frame" :
          for kk, vv in strategies[strategy]["stateMap"].items(): 
            print("\t", kk)
            for kkk, vvv in vv.items():
              print("\t\t", kkk)
              for kkkk,  vvvv in vvv.items():
                print("\t\t\t", kkkk, vvvv)


      #NICE, producing proper stateMap now......

    """ This section runs strategies....."""
    print("We have successfully made pandas df, and statmap, \n\tnow waitting to go in forever loop")
    if not isCsv: sleep(30)
    
    #Forever Loop
    while True:
      index____ +=1
      
      #if isDebug:  print(index____, "index____ before for loop")
      
      for strategy_name, dict_of_functions in strategies.items():
        #if isDebug: print(index____, "index____ this should not change from above in for loop")
        
        (dict_of_curr_to_pandas_df, actualChangeToPandasDict, dictOf_incomplete_data) = strategies[strategy_name]["get_new_pandas_info"](
                secretInfo,    #For bearer Token and account info for Oanada
                productoinMode, #Decides to use API 
                isCsv,          #Decides to use csv
                debugMode,      #Add print/logging statements
                strategies[strategy_name]["currencies_in_this_stratgey"],  #Not sure why this is needed
                strategies[strategy_name]["pandas_df"])                    #Not 
        
        if debugMode:  frameinfo = getframeinfo(currentframe()); print(frameinfo.filename, frameinfo.lineno, "result_of_new_pandas_info", dict_of_curr_to_pandas_df, actualChangeToPandasDict)
        
        #TODO
        #TODO
        #TODO
        #Check if this dict was populated
        #If it was, check if we hit limit order/exit/stop losss
        #if len(list(dictOf_incomplete_data)) > 0:
          #I need to check all current orders I am in
          #Check if my stop loss level was ever hit below
          #If so, exit order
          #Well I have some issues here
          #First I need to first optimize this value
          #Second I need to store these? Maybe Hard code them in
          #I am realizing that I should optimize for that first
          #Which means two things.
          #I should run this on one shell bash 
          #And my backtesting in another


        #NOTE it should probably run all these functions
        #Because isAnUpdate is logic to this specific strategy
        #TODO take this if statement out, it bloats this area
        
        if actualChangeToPandasDict:
            strategies[strategy_name]["pandas_df"] = dict_of_curr_to_pandas_df
            
            if isDebug: #Can I abstract this out, I don't want to see these 4 lines of code here 
              frameinfo = getframeinfo(currentframe())
              print(frameinfo.filename, frameinfo.lineno,
                    "before statemap for", 
                    strategy_name, strategies[strategy_name]["stateMap"]['15min']['EUR_USD'])

            #Update StateMap off new data
            #TODO rename isSaucy, I do not like it, I think it is another for isSuccess
            #Probably should throw an error
            (strategies[strategy_name]["stateMap"], isSaucy) = strategies[strategy_name]["update_state_map"](
                        isDebug,
                        isCsv,
                        dict_of_curr_to_pandas_df, 
                        strategies[strategy_name]["stateMap"],
                        strategies[strategy_name]["currencies_in_this_stratgey"],
                        index____
                        )
            if isDebug:
              frameinfo = getframeinfo(currentframe())
              print(frameinfo.filename, frameinfo.lineno,
                    "after statemap for strategies[strategy_name][stateMap][15min][EUR_USD]", 
                    strategy_name, strategies[strategy_name]["stateMap"]['15min']['EUR_USD']
                    )


            #
            #Decide to make a new trade based off updated stateMap
            #
            

            ##TODO more logic for exitting trades, especially stop losses
            ##And info about current prices
            ##Might need to pass the pandas df in
            ## or some other logic 
            #The return in tuple (dict , bool, bool)
            (tradesToMake, decideToMakeTrade_, decideToExit) = strategies[strategy_name]["deciding_to_make_trade"](
                        strategies[strategy_name]["stateMap"],
                        strategies[strategy_name]["times_frame_this_stratgey_is_focused_on"],
                        isDebug,
                        isLiveTrading
                        )
            

            #This is for tracking to analyze the bot decision on trades 
            #Log_trades_decided_on
            #I think logging would be helpful, there should be different logging for live trading
            #VS backtesting, back testing logging would be to verbose, but this is good to log for live trading
            if decideToMakeTrade_ :
              #NOTE THIS IS ONLY FOR THis strategy and should be updated
              #print(tradesToMake)
              log_trades_strategy_signaled_to_make = { shouldBeTimeStamp: shouldBeDict["trades_to_enter_singal"] for shouldBeTimeStamp, shouldBeDict in tradesToMake.items() if "trades_to_enter_singal" in  list(shouldBeDict.keys())} 
              
              strategies[strategy_name]["log_trades_I_decided_to_make"].append(
                log_trades_strategy_signaled_to_make)
              if isLiveTrading: print("decided to make trade, add to a log file")
              #Ideally A json, that just keeps a log of what is happned
              #Something that is easily analyze-able via pandas and note book
              #That can be written to file
              #   
            # if len(tradesToMake) != 0: #TODO remove ? Old code I am not sure if I need
            #   strategies[strategy_name]["trades_I_decided_to_make"].append(tradesToMake['trades_to_enter_singal']) 

              (orders_made, trades_to_make_dict) = strategies[strategy_name]["make_orders"](
                          isCsv,
                          decideToMakeTrade_,
                          tradesToMake, #<time <"decidetoMake" : [(currencies and stuff)]>>
                          bearerTokenOanda,
                          accountNumOanda,
                          isLiveTrading
                          )

              #Proccess Trades Made
              strategies[strategy_name]["curr_trades_I_am_in"] = strategies[strategy_name]["proccess_orders_made"](
                          orders_made,
                          strategies[strategy_name]["curr_trades_I_am_in"]
                          )

            #Exit trades
            #Todo this should have a stop loss element to it
            if decideToExit:  #and if_Iam_in_a_Trade:
              if isDebug: print("decideToExit ?", strategies[strategy_name]["curr_trades_I_am_in"])
              result_from_exit_orders  = strategies[strategy_name]["proccess_orders_to_exit"](
                isCsv,
                tradesToMake,  #<time <"decidetoMake" : [(currencies and stuff)]>>
                strategies[strategy_name]["curr_trades_I_am_in"], #TODO  change this to curr_trades_in
                bearerTokenOanda,
                accountNumOanda
                )
            
              if len(list(result_from_exit_orders.keys())) > 0: strategies[strategy_name]["list_of_results_from_orders_this_is_test"].append(result_from_exit_orders) 

              (strategies[strategy_name]["curr_trades_I_am_in"], stats_to_judge_preformance)  = strategies[strategy_name]["update_currOrders_from_exit_result"](
                result_from_exit_orders,
                strategies[strategy_name]["curr_trades_I_am_in"]
                )
              
              
              if len(stats_to_judge_preformance) > 0: strategies[strategy_name]["list_of_final_stats"].append(stats_to_judge_preformance) 
              
            #FOR LOOP sanity check prints
            if sanityCheck_only_print_a_few_loops[0]: 
              sanityCheck_only_print_a_few_loops[1]+=1
              if sanityCheck_only_print_a_few_loops[1] % 3 == 0:
                for strat_name, dddd in strategies.items():
                  for timeFrame, dictOfCurrency in  strategies[strat_name]["curr_trades_I_am_in"].items(): 
                      for currrrencccc, stats in dictOfCurrency.items():
                        if len(stats)  > 0: print("Trade I am in",stats)


                print("Holly SHit we are doing updates")
            if isDebug: print("Holly SHit we did an update")

      if isCsv: printResults(isDebug, index____ , strategies)
      if not isCsv: sleep(1*60)





