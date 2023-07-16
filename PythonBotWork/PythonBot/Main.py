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
import logging

### Not sure if I am using the below imports
from pandas_datareader import data
import mplfinance as mpf



## Import my local files
runningInGoogleColab = False
if runningInGoogleColab:
  print(os.getcwd())
  os.chdir("NoGambleNoFuture")
  print(os.getcwd())

from Util.LoggingHelpers.LoggingHelper                       import *
from Strategy_Setup.Strategy_Setup                           import *
from Account_Info_Setup                                      import *

from Step1InitDf.InitDf_only_correlated_trade_at_once        import *
from Util.Step12PrintOutResults.Step12PrintOutResults        import printResults

from API_calls                                               import *

from InitStateMap.InitStateMap_for_correlated_excution       import *
from UpdatePandasDf.UpdatePandasDf_currencies_move_together  import *
from UpdateStateMap.UpdateStateMap_correlated_move_only      import *

from DecideToMakeTrade.DecideToMakeTrade                     import *
from MakeTrades.MakeTrades                                   import *
from ProccessTradesMade.ProccessTradesMade                   import *
from ExitTrades.ExitTrades                                   import *

from Dashboard.Create_candle_chart                           import *


"""
Main in broken into three sections

1. Init the basic variables, like debug mode, production mode, 
2. Init data structure that holds state of strategy
3. In a forever loop that updates every _ seconds

"""


def main():



    """
    Setup logging
    We have logging for 
    a. deciding to make trades
    b. trades
    c. attempting
    d. everything logger  
    """
    # logging.basicConfig(filename='example2.log',
                        # format='%(asctime)s : %(levelname)s : %(message)s', 
                        # encoding='utf-8', 
                        # level=logging.DEBUG)
    # Create a logs directory if it doesn't exist
    log_folder = 'Util/Logs'
    if not os.path.exists(log_folder):os.makedirs(log_folder)
    # Create loggers
    deciding_logger = logging.getLogger('deciding_logger')
    trades_logger = logging.getLogger('trades_logger')
    attempting_logger = logging.getLogger('attempting_logger')
    everything_logger = logging.getLogger('everything_logger')

    # Configure loggers
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_level = logging.INFO
    
    # Create file handlers for each logger
    deciding_handler = logging.FileHandler(os.path.join(log_folder, 'deciding.log'))
    trades_handler = logging.FileHandler(os.path.join(log_folder, 'trades.log'))
    attempting_handler = logging.FileHandler(os.path.join(log_folder, 'attempting.log'))
    everything_handler = logging.FileHandler(os.path.join(log_folder, 'everything.log'))
    
    # Set the log format for each handler
    deciding_handler.setFormatter(logging.Formatter(log_format))
    trades_handler.setFormatter(logging.Formatter(log_format))
    attempting_handler.setFormatter(logging.Formatter(log_format))
    everything_handler.setFormatter(logging.Formatter(log_format))
    
    # Add handlers to the respective loggers
    deciding_logger.addHandler(deciding_handler)
    trades_logger.addHandler(trades_handler)
    attempting_logger.addHandler(attempting_handler)
    everything_logger.addHandler(everything_handler)
    
    # Set the log level for everything logger
    everything_logger.setLevel(logging.DEBUG)
    
    # Now you can use the loggers in your trading bot
    deciding_logger.info('Deciding to make trades...')
    attempting_logger.info('Attempting to perform trades...')
    trades_logger.info('In-trade updates...')
    everything_logger.info('Logging everything...')



    """Bearer Token setup"""
    (bearerTokenOanda, accountNumOanda) = getBearAndAccount() #Should pass these values around so it is easier to  #Pass to a google colab
    secretInfo = {"bearerTokenOanda" : bearerTokenOanda, "accountNumOanda": accountNumOanda }

    index____               = 300 #Only used for back testing with csv files


    #TODO clean this up, I have too many arguements here
    useAPI_for_data_and_make_trades_on_exchange_ = False
    sanityCheck_only_print_a_few_loops           = [True, 0]

    #Remove these two, you do not need both
    makeRealMoneyTrades         = False
    makeOrders                  = True     #What does this do?

    useAPIsToPopulatePandasInfo        = True
    productoinMode                     = True   
    isLiveTrading                      = productoinMode


    debugMode                          = False
    shouldSleepForDebugPurposes        = True #This just sleeps in certain places, Only in places in code if debugmode is on

    isCsv                   = False

    debugMode               = False
    isDebug                 = debugMode


    #TODO set this up so it can correctly import files and libraries more seemlessly
    runningInANoteBook =    False
    print("Initial variable setup complete")
    strategies  = makeStrategies()
    print("strategy setup compltee")
    logging.info('Initial variable setup complete')



    #TODO Move the init logic outside here
    #I do not want to be looking at it
    """ This Section is setting up the StateMaps, and Pandas DF for each strategy/robot"""
    #  strategies[k]
    for strategy in strategies.keys():
      strategies[strategy]["pandas_df"] = strategies[strategy]["init_pandasDf"](
        productionMod       = useAPIsToPopulatePandasInfo,
        isCsv               = isCsv,
        list_of_currnec     = strategies[strategy]["currencies_in_this_stratgey"],
        list_of_time_frames = strategies[strategy]["times_frame_this_stratgey_is_focused_on"],
        secretInfo          = secretInfo)
      
      
      #initStateMaps -> 
      #init_stateMap_for_only_correlatred_trades -> 
      #    createStateMap_for_only_correlatred_trades . createStateMap_for_only_correlatred_trades
      strategies[strategy]["stateMap"]  = strategies[strategy]["initStateMaps"](
        isCsv,
        debugMode,
        strategies[strategy]["pandas_df"],
        strategies[strategy]["currencies_in_this_stratgey"]
        )
      

      print("strategy", strategy)
      #TODO clean this up so there isn't an if statement here
      if productoinMode:

         (strategies[strategy]["stateMap"], _ )  = update_state_map_from_new_pandas_info(
            isDebug,
            isCsv,                                                                  
            strategies[strategy]["pandas_df"],
            strategies[strategy]["stateMap"],
            strategies[strategy]["currencies_in_this_stratgey"],
            0,
            False)
      else:
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
        #But do not move this until you have it working properly for all stragegies, this should always be happening.
        #This is a safe check that should always be happening in production
        #TODO this shouldn't be abstracted out, this should be here, but run for every run.....
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


    ##[wip] This is the charts that show up in the beginning, #TODO  I want this live and showing P/L as well
    test_show_candle_chart(strategies)
    

    """ This section runs strategies....."""
    print("We have successfully made pandas df, and statmap, \n\tnow waitting to go in forever loop")
    if not isCsv: sleep(30)
    
    #MAJOR TODO
    #Before going into a forever loop, I should have check that
    #The data has been made correctly (populated correctly, correct size)


    #Forever Loop
    while True:
      index____ +=1 #TODO I do not like the index approach. Is there another way to make this possible for debug mode?
      
      for strategy_name, dict_of_functions in strategies.items():
        
        
        res___ = strategies[strategy_name]["get_new_pandas_info"](
                secretInfo,    #For bearer Token and account info for Oanada
                productoinMode, #Decides to use API 
                isCsv,          #Decides to use csv
                debugMode,      #Add print/logging statements
                strategies[strategy_name]["currencies_in_this_stratgey"],  #Not sure why this is needed
                strategies[strategy_name]["pandas_df"],
                strategies[strategy_name]["times_frame_this_stratgey_is_focused_on"], #This shouldn't be needed, this should be filtered out in the future
                True
                )               
        (dict_of_curr_to_pandas_df, actualChangeToPandasDict, dictOf_incomplete_data)  = res___
        if debugMode:  frameinfo = getframeinfo(currentframe()); print(frameinfo.filename, frameinfo.lineno, "result_of_new_pandas_info", dict_of_curr_to_pandas_df, actualChangeToPandasDict)
        
        #if an upadte actually happened in pandas df then
        #check if we hit limit order/exit/stop losss
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
            #Update pandas df
            strategies[strategy_name]["pandas_df"] = dict_of_curr_to_pandas_df
            
            #Update StateMap off new data
            #isSaucy === isSuccess #TODO can I get rid of isSaucy?
            (strategies[strategy_name]["stateMap"], isSaucy) = strategies[strategy_name]["update_state_map"](
                        isDebug,
                        isCsv,
                        dict_of_curr_to_pandas_df, 
                        strategies[strategy_name]["stateMap"],
                        strategies[strategy_name]["currencies_in_this_stratgey"],
                        index____ #If using a csv file we actually index throw the pandas df
                        )

            
            ##TODO more logic for exitting trades, especially stop losses, And info about current price 
            """ 
            #Now that we updated the statemap, we see if we need to excute a trade
            Decide to make a new trade based off updated stateMap
            
            Returns: triple (dict , bool, bool)
              - dict: key = timeframe and value list of 
              - bool: let's us know if a trade should be made
              - bool: let's us know if an exit trade signal was found.
            """
            (tradesToMake, decideToMakeTrade_, decideToExit) = strategies[strategy_name]["deciding_to_make_trade"](
                        deciding_logger,
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
              # Basically log file for trades, for everything for seperate things.   
              # if len(tradesToMake) != 0: #TODO remove ? Old code I am not sure if I need
              #   strategies[strategy_name]["trades_I_decided_to_make"].append(tradesToMake['trades_to_enter_singal']) 

              (orders_made, trades_to_make_dict) = strategies[strategy_name]["make_orders"](
                          attempting_logger,
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

            ##Exit trades #TODO this should have a stop loss element to it
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
      showTradesIn(trades_logger, strategies)



# fig_for_stats, axs_for_stats = plt.subplots(amount_of_graphs+1)

if __name__ == "__main__":
    main()





