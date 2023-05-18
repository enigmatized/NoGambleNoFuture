
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

from API_calls.Oanada.Oanda import *  


#What should this return?
#It's own pandas df
#So arguements should be

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
def get_new_pandas_info_update_pandas_df_henksi_3_currencies_move_together(
                            secret_info,
                            isProd, 
                            isCsv,
                            isDebug, 
                            currnecies, 
                            dict_of_currentPandasDf):
  if isProd:
    
    #Make a dictionary for json resonses?
    #Making (key=currency, value=json)
    dict_json_respone_shorter_time_frame = defaultdict(dict)
    dict_of_pandas_incomplete_data = defaultdict(dict)
    actualChange = False
    #Get candles for each currency, api calls to broker
    for currenC in currnecies: 
        (json_from_exchange, was_a_success) = getCandles_fromOanada(currenC, count = "3", bearerToken = secret_info["bearerTokenOanda"], accountNum =secret_info["accountNumOanda"] )
        if not was_a_success: pass
        else : 
          # dict_of_tuple_of_pandas_formated_with_complete_and_incomplete[currency] = 
          #for currnecy, tuple_of_pandas in dict_of_tuple_of_pandas_formated_with_complete_and_incomplete.items():
              (completePandas, incompleteSomething, is_incomplete, restOfData) = createPandasDfFromAPI3(json_from_exchange)
              
              #Use the incomplete data to see if we have gone past limit orders
              if not restOfData.empty: dict_of_pandas_incomplete_data[currenC] = restOfData

              (inCompletePandasDf, isIncomplete) = incompleteSomething
              if isDebug :print("THIS PANDAS SHOULD ALWASY BE SIZE 1, so (_, 1)", inCompletePandasDf.shape)
              if dict_of_currentPandasDf[currenC].tail(1).equals(completePandas.tail(1)):
                  pass
              
              
              else: 
                if isDebug: print("dict_of_currentPandasDf[currenC].tail(1).equals(completePandas)", dict_of_currentPandasDf[currenC].tail(1))
    
                dict_of_currentPandasDf[currenC] = pd.concat(
                    [dict_of_currentPandasDf[currenC],
                     completePandas
                    ]
                    ).drop_duplicates()
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
def createPandasDfFromAPI3(json_response_from_oanda_API): 
  # print(tempTester)
  #getunCompleteCandles returns tuple of  (dict<key ,value>, Bool if incomplete)
  (pandas_df,incomplete)= getunCompleteCandles(json_response_from_oanda_API) #  getunCompleteCandles :: json_of_api -> (<dictionary   >, Bool)
  
  #Turn dictionary into pandasDf
  mainDf  = pd.DataFrame(pandas_df).T 
  
  #make column heikin_ashi_open
  mainDf['heikin_ashi_open']  = 0.5 *( mainDf['close'].shift(1) +mainDf['open'].shift(1) )
  
  #TODO write a test to make sure all this is correct
  #Get rid of the first value that is NA as a result of the above operation
  #From Pandas docs :
  #                For negative values of n, 
  #                this function returns all rows 
  #                except the first |n| rows, equivalent to
  mainDf = mainDf.tail(-1) # So this gets rid of the first column because the above operation produces a NA value in first comlumn

  if incomplete: 
    #so if incomplete get rid of the last row
      mostRecentData = mainDf.tail(1) #Get last row aka incomplete data 
      final_mainDf   = mainDf.head(-1) #Remove the last row
      final_incompleteData = (mainDf.tail(-1), incomplete)  
  else:
      mostRecentData       =  pd.DataFrame()
      final_mainDf         =  mainDf
      final_incompleteData = (mainDf, incomplete) 
      

  #Not I beleive except for the first inti call,
  #I think this pandas def return should only be size of one
  
  #TODO Why am I passing incomplete twice?
  return (final_mainDf,  final_incompleteData, incomplete, mostRecentData)





def getunCompleteCandles(json_Instrument_Info, isDebug=False):#Each function/definiton will be different
        innderDict = defaultdict(dict)
        
        inst    = json_Instrument_Info['instrument']
        grans   = json_Instrument_Info['granularity']
        candles = json_Instrument_Info['candles']
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
            # else:
            #     strObjDate = x["time"]
            #     time_Of_this_Candle                                       = datetime.strptime(strObjDate[:19], '%Y-%m-%dT%H:%M:%S')
            #     incompleteDict[time_Of_this_Candle]["close"]              = float(x["mid"]['c'])
            #     incompleteDict[time_Of_this_Candle]["open"]               = float(x["mid"]['o'])
            #     incompleteDict[time_Of_this_Candle]["high"]               = float(x["mid"]['h'])
            #     incompleteDict[time_Of_this_Candle]["low"]                = float(x["mid"]['l'])
            #     incompleteDict[time_Of_this_Candle]["heikin_ashi_close"]  = 0.25 * (float(x["mid"]['o']) + float(x["mid"]['c']) + float(x["mid"]['l']) + float(x["mid"]['h']))
            #     incompleteDict[time_Of_this_Candle]["volume"]             = int(x["volume"])
            #     incompleteDict[time_Of_this_Candle]["time"]               = (time_Of_this_Candle - timedelta(hours=4)).time() 
              



                
                #print(type(innerDf[(inst, grans)]["WhyDoesThisNotWork"] ) )
        #return (innderDict, incompleteDict)
        return (innderDict, notComplete)