
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


#FOR TESTING in python notebook locally
# pythonLocalNoteBook = True
# if pythonLocalNoteBook:
#   print(os.getcwd())
#   # os.chdir("NoGambleNoFuture")
#   os.chdir("..")
#   print(os.getcwd())


from API_calls.Oanada.Oanda import *  



"""
isProd = Bool
isCsv  = Bool #Means weather to get data source from local csv files for  back testing
currnecies = [Str] #List of currency pairs use in the api
currentPandasDf = 
index = only needed if in backtesting mode and using csv data
        #NOTE: if I am in csv mode, this shouldn't update the actual pandas 
        #It should update the index
        #I think this should retunrn a update pandasDf, so if I need to do something


returns dictionary of (pandasDf, actualChange)

"""
#What the fuck is happening here, this is messy as fuck
def get_new_pandas_info_update_pandas_df_henksi_3_currencies_move_together(
                            secret_info,
                            isProd, 
                            isCsv,
                            isDebug, 
                            currnecies, 
                            dict_of_currentPandasDf,
                            times_frame_this_stratgey_is_focused_on = [],
                            needs_update_=False): #This needs to be added to back testsing
  #My production is starting to differ a lot from csv
  #Next time I run csv  I will have a lot of problems
  if isProd:
    
    #Make a dictionary for json resonses?
    #Making (key=currency, value=json)
    dict_json_respone_shorter_time_frame = defaultdict(dict)
    dict_of_pandas_incomplete_data = defaultdict(dict)
    actualChange = False
    
    #Get candles for each currency, api calls to broker
    time_frames_in_pandas = list(dict_of_currentPandasDf.keys())#Note just becayse pandas time frame is in dict doesn't mean we are trading or need to update it
    time_frames = [x for x  in time_frames_in_pandas if x in  times_frame_this_stratgey_is_focused_on]
    
    for time_frame in time_frames:
      for currenC in currnecies: 
          (json_from_exchange, was_a_success) = getCandles_fromOanada(currenC, count = "3", bearerToken = secret_info["bearerTokenOanda"], accountNum =secret_info["accountNumOanda"] )
          if not was_a_success: pass #If this passes, does this mean I mess up my pandasDf?
          else : 
            # dict_of_tuple_of_pandas_formated_with_complete_and_incomplete[currency] = 
            #for currnecy, tuple_of_pandas in dict_of_tuple_of_pandas_formated_with_complete_and_incomplete.items():
                (completePandas, (candles_of_data_not_compelte_yet,is_incomplete__), is_incomplete) = createPandasDfFromAPI3(json_from_exchange)

                #Use the incomplete data to see if we have gone past limit orders
                if is_incomplete: dict_of_pandas_incomplete_data[currenC] = candles_of_data_not_compelte_yet

                (inCompletePandasDf, isIncomplete) = (candles_of_data_not_compelte_yet,is_incomplete__) #TODO get rid fo this

  #_----------------THIS PRINT OUT IS HELPFUL FOR OLD DEBUGGING PURPOSES ----------------
                print("--------------------")
                #print("----------------")

                #print(" completePandas.tail(1)", list(completePandas.keys()), "type", type(completePandas))
                switch__ = True
                for rrr, rowsss in completePandas.tail(1).iterrows():
                    #print("\Wait ", rrr)
                    for column_name, column_value in rowsss.items():
                      #print("dict_of_currentPandasDf[time_frame].keys()",     list((dict_of_currentPandasDf[time_frame].keys())), "time_frame", time_frame, currenC)
                      for rrrr, rowssss in dict_of_currentPandasDf[time_frame][currenC].tail(1).iterrows():
                          if switch__ : 
                            # print("The index should be the same", 
                            #       dict_of_currentPandasDf[time_frame][currenC].tail(1).index[-1],
                            #       completePandas.tail(1).index[-1],
                            #       dict_of_currentPandasDf[time_frame][currenC].tail(1).index[-1] == completePandas.tail(1).index[-1]
                            #       )
                            # print("Index?", "API", rrr, "main df", rrrr); 
                            switch__ = False
                          for column_name_, column_value_ in rowssss.items():
                              if column_name == column_name_ : print(f"Column: {column_name}, ValueAPI: {column_value}, ValueMainDf: {column_value_}")
                      # print(f"Column: {column_name}, Value: {column_value}")
                      # print(f"Column: {column_name}, Value: {column_value}")
                #print()
                print("can you tell me why this have NA values? dict_of_currentPandasDf[time_frame][currenC].tail(1)", dict_of_currentPandasDf[time_frame][currenC].tail(1))
                # for rrr, rowsss in dict_of_currentPandasDf[time_frame][currenC].tail(1).iterrows():
                # #     print("\trrr", rrr)
                #     for column_name, column_value in rowsss.items():
                #       print(f"Column: {column_name}, Value: {column_value}")

                #print("--------------------")

  #______________________________BELOW IS REAL LOGIC __________________________
                if isDebug :print("THIS PANDAS SHOULD ALWASY BE SIZE 1, so (_, 1)", inCompletePandasDf.shape)
                
                if dict_of_currentPandasDf[time_frame][currenC].tail(1).index[-1] == completePandas.tail(1).index[-1]:
                    print("This should be happening often")
                    pass
                
                
                else: 
                  if isDebug: print("dict_of_currentPandasDf[time_frame][currenC].tail(1).equals(completePandas)", dict_of_currentPandasDf[time_frame][currenC].tail(1))
                  print("This should be happening less often")
                  
                  # for i, val in dict_of_currentPandasDf[time_frame][currenC].tail(1).iterrows():
                      

                  print("-----------------------")
                  dict_of_currentPandasDf[time_frame][currenC] = pd.concat(
                      [dict_of_currentPandasDf[time_frame][currenC],
                      completePandas.tail(1)
                      ]
                      ).drop_duplicates()
                  
                  print("--------")


                  print("------")
                  #THIS FUNCTION SHOULD BE TAKEN OUT
                  #dict_of_currentPandasDf[k] = make_current_state2(completePandas, dict_of_state_maps[currency])
                  actualChange = True
      
    return (dict_of_currentPandasDf, actualChange, dict_of_pandas_incomplete_data)
  if isCsv: #TODO, decide to index here or in the next function
      return (dict_of_currentPandasDf, True, None) #TODO I can add this functionality while using small time frames


    
def check_if_new_pandas_info_for_correlated_trade_strat():

  """
  createPandasDfFromAPI3 
     takes json_api_data_response 



     @return (pandas_df_complete_data, incomplete_data, Bool)
  """
def createPandasDfFromAPI3(json_response_from_oanda_API, isDebug = False): 
  #getunCompleteCandles returns tuple of  (dict<key ,value>, Bool if incomplete)
  (pandas_df,incomplete)= getunCompleteCandles(json_response_from_oanda_API) #  getunCompleteCandles :: json_of_api -> (<dictionary   >, Bool)
  


  #Turn dictionary into pandasDf
  mainDf  = pd.DataFrame(pandas_df).T 
  
  if isDebug: print("Before adding seikin opne", mainDf) 
  #make column heikin_ashi_open TODO make sure this is right?
  mainDf['heikin_ashi_open']  = 0.5 *( mainDf['close'].shift(1) +mainDf['open'].shift(1) )
  if isDebug: print("After adding heikin_ashi_open", mainDf)

  #TODO write a test to make sure all this is correct
  #Get rid of the first value that is NA as a result of the above operation
  #From Pandas docs :
  #                For negative values of n, 
  #                this function returns all rows 
  #                except the first |n| rows, equivalent to
  mainDf = mainDf.tail(-1) # So this gets rid of the first column because the above operation produces a NA value in first comlumn

  if isDebug: print(mainDf) 
  #So this mainDf should only be size two now
  if incomplete: #so if incomplete get rid of the last row
      final_mainDf   = mainDf.head(-1) #Since two rows, first row is complete, last is not
      # final_mainDf   = final_mainDf.head()
      #Remove the last row
      final_incompleteData = (mainDf.tail(1), incomplete)  #Get last row aka incomplete data 
  else:
      final_mainDf         =  mainDf
      final_incompleteData = (mainDf, incomplete) 
      

  
  #TODO Why am I passing incomplete twice?
  return (final_mainDf,  final_incompleteData, incomplete)




def getunCompleteCandles(json_Instrument_Info, isDebug=False):
        innderDict = defaultdict(dict)
        
        inst             = json_Instrument_Info['instrument']
        grans            = json_Instrument_Info['granularity']
        candles          = json_Instrument_Info['candles']
        time_to_subtract = datetime.strptime("4:00:00", "%H:%M:%S")
        
        incompleteDict =  defaultdict(dict)
        notComplete = False
        
        for x in candles:
            
                strObjDate = x["time"]
                time_Of_this_Candle                                   = datetime.strptime(strObjDate[:19], '%Y-%m-%dT%H:%M:%S')
                innderDict[time_Of_this_Candle]["close"]              = float(x["mid"]['c'])
                innderDict[time_Of_this_Candle]["open"]               = float(x["mid"]['o'])
                innderDict[time_Of_this_Candle]["high"]               = float(x["mid"]['h'])
                innderDict[time_Of_this_Candle]["low"]                = float(x["mid"]['l'])
                innderDict[time_Of_this_Candle]["heikin_ashi_close"]  = 0.25 * (float(x["mid"]['o']) + float(x["mid"]['c']) + float(x["mid"]['l']) + float(x["mid"]['h']))
                innderDict[time_Of_this_Candle]["volume"]             = int(x["volume"])
                innderDict[time_Of_this_Candle]["time"]               = (time_Of_this_Candle - timedelta(hours=4)).time()
                if not x["complete"]: notComplete = True
                if isDebug: print("not x[\"complete\"]", not x["complete"], x["complete"], type(x["complete"]), innderDict[time_Of_this_Candle]["time"])
        return (innderDict, notComplete)