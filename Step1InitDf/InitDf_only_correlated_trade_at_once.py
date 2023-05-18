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
from urllib.error import HTTPError


### ALL THESE FUNCIONS ARE RELATED TO THE IniitDF SECTION IN MAIN FUNCTION
#THIS Code block is for getting data from the exchange and setting up the first call and others calls

#TODO  modify for candle count and grandulatiry
#TODO better documentation
#THIS SHOULD NEVER throw an error and error out
#Not stop the program
def getCandles_aka_callToUpdateInfo(currency, count = "3", bearerToken = None, accountNum = None):
    if bearerToken == None or accountNum == None : raise ValueError('Calling the APIs without token/account info is a very bad thing, are you really prepared for this?')
    try:
        r = requests.get('https://api-fxtrade.oanda.com/v3/instruments/'+currency +'/candles?count='+ count +'&price=M&granularity=M15',
            headers= { 'Content-Type': 'application/json','Authorization': 'Bearer ' + bearerToken} #Correct this to be read from file
            )
        r.raise_for_status()
        return (r.json(), True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
        return ( {}, False)
    except Exception as err:
        print(f'Other error occurred in getCandles_aka_callToUpdateInfo: {err}')
        return ( {}, False)
    print("Something went wrong in getCandles_aka_callToUpdateInfo!!!!!!!!!!!!!!!")
    return ("", False)

#Note 15m * 16 = 4hrs 

def firstCallToInitState(currency, secretInfo): 
  #Special case to start the state,
  #This should not return a tuple object and I call it here
  #I should have a check or throw an error
  #If this is bad then the entire project is bad
  return getCandles_aka_callToUpdateInfo(
     currency,
     "80",
     secretInfo["bearerTokenOanda"],
     secretInfo["accountNumOanda"])[0]  #Why is this [0], what is going here?




""" """
def first_call_to_get_data_from_exchange(productoinMod, currencys_, secretInfo):
  if productoinMod:
    resDict = {}
    for currency_pair in currencys_: 
       print("currenc", currency_pair,resDict )
       resDict[currency_pair] = firstCallToInitState(currency_pair, secretInfo)
       print("currenc", currency_pair,resDict )
    return resDict
  else : 
    #TODO implemnt your Test
    return {}


def setup_pandas_df_forall_currencies(productoinMod, diction, currencies_if_not_production):
  if productoinMod:
    print("SHould not be getting here atm")
    print(diction)
    resD = {}
    for currency, json_response_from_api_resquest in diction.items(): resD[currency] = createPandasDfFromAPI(json_response_from_api_resquest)
    return resD
  else : 
    return getPandasFromCSVFiles(currencies_if_not_production) 


#This function is tricky
#In the future I might want to think about modifying pandas dataframes to meet the conditions of certain strategies
def getPandasFromCSVFiles(currencies_if_not_production, directory_location= "./BackTestingData"):
  
  #TODO should throw an error if I do not find all the dfs I am looking for 
  #

  dict_currencies_if_not_production__ = {x.replace("_", "") : x for x in currencies_if_not_production}
  
  currencies_if_not_production = [x.replace("_", "") for x in currencies_if_not_production] + currencies_if_not_production
  
  print("Why are we not here?")
  CSVfiles = []
  for file in os.listdir(directory_location): 
    if file.endswith(".csv"): 
      CSVfiles.append(file)
  print("filed read", CSVfiles)

  unixTimeConverter = lambda x : (datetime.fromtimestamp(x)).strftime('%Y-%m-%d %H:%M:%S')
  unixTimeConverterNoDateJustTime = lambda x : (datetime.fromtimestamp(x)).time()


  allDfs = {}

  for x in CSVfiles:
    matchingCurrnecies = [ y for y in currencies_if_not_production if (y in x)]
    if len(matchingCurrnecies) > 0: 
      [currency____] =  matchingCurrnecies #This should only ever 
      dfTemp = pd.read_csv( x) #x if "." != directory_location else directory_location+x)
      dfTemp['estTime']  = dfTemp['time'].apply(unixTimeConverter)
      dfTemp['timeOnly'] = dfTemp['time'].apply(unixTimeConverterNoDateJustTime)
      dfTemp['heikin_ashi_open']  = 0.5 *( dfTemp['close'].shift(1) +dfTemp['open'].shift(1) )
      dfTemp['heikin_ashi_close'] = dfTemp.apply(lambda row: 0.25 * (row.open + row['close'] + row['high'] + row['low'])  , axis = 1)
  
      dfTemp = dfTemp.tail(-1)
      dfTemp = dfTemp.head(-1)
      allDfs[dict_currencies_if_not_production__[currency____]]  = dfTemp


  #print("allDFS", allDfs)
  return make_dict_of_pandasDfs_the_same_for_backtesting(allDfs)



def make_dict_of_pandasDfs_the_same_for_backtesting(pandasDf):
  (smallestTime, largestTime) = (-float('inf'), float('inf')) 

  dicOfCurrency_to_high_low = {}
   
  for k, v in pandasDf.items():
      lowestTimeInDf  = v.iloc[0]["time"]
      highestTimeInDf = v.iloc[-1]["time"]

      if highestTimeInDf < largestTime:   largestTime = highestTimeInDf 
      if lowestTimeInDf  > smallestTime:  smallestTime = lowestTimeInDf 

      dicOfCurrency_to_high_low[k] = {"highTime": highestTimeInDf , "lowTime": lowestTimeInDf }
      
      print("Lowest and highest time frame",(smallestTime, largestTime) )
      print("Show where lowest time frame is on index", v.index[v['time'] == smallestTime].tolist(), lowestTimeInDf)
      print("Show where lowest time frame is on index", v.index[v['time'] == largestTime].tolist(),  highestTimeInDf)
  

  for k, dff in pandasDf.items():
     index_ = pandasDf[k].index[pandasDf[k]['time'] == smallestTime].tolist()[0]
     print("WHAT THE FUCK IS THIS DOING?", index_ )
     print(dff.shape, " after  df.iloc[index_:].shape",   (dff.iloc[index_:]).shape)
     pandasDf[k] =  pandasDf[k].iloc[index_:]

     index_ = pandasDf[k].index[pandasDf[k]['time'] == largestTime].tolist()[0]
     pandasDf[k] =  pandasDf[k].iloc[:index_ -1 ]
  return pandasDf

     

def createPandasDfFromAPI(json_of_currency):
  # print("-----------------------------")
  # print(json_of_currency)
  ddd     = prep_json_from_API_for_pandas(json_of_currency)
  mainDf  = pd.DataFrame(ddd).T
  mainDf['heikin_ashi_open']  = 0.5 *( mainDf['close'].shift(1) +mainDf['open'].shift(1) )
  
  #Get rid of the first value that is NA as a result of the above operation
  mainDf       = mainDf.tail(-1) 
  final_mainDf = mainDf.head(-1)
  
  # mainDf.head()
  # mainDf.tail()
  # print("----- createPandasDfFromAPI---")
  # print(final_mainDf)
  return final_mainDf


def prep_json_from_API_for_pandas(json_Instrument_Info):#Each function/definiton will be different
        innderDict = defaultdict(dict)
        
        inst    = json_Instrument_Info['instrument']
        grans   = json_Instrument_Info['granularity']
        candles = json_Instrument_Info['candles']
        time_to_subtract = datetime.strptime("4:00:00", "%H:%M:%S")
        # unixTimeConverter = lambda x : (datetime.fromtimestamp(x)).strftime('%Y-%m-%d %H:%M:%S')
        # unixTimeConverterNoDateJustTime = lambda x : (datetime.fromtimestamp(x)).time()

        #print(time_Of_this_Candle)
        for x in candles:
            if x["complete"]:
                strObjDate = x["time"]
                time_Of_this_Candle = datetime.strptime(strObjDate[:19], '%Y-%m-%dT%H:%M:%S')
                innderDict[time_Of_this_Candle]["close"]               = float(x["mid"]['c'])
                innderDict[time_Of_this_Candle]["open"]                = float(x["mid"]['o'])
                innderDict[time_Of_this_Candle]["high"]                = float(x["mid"]['h'])
                innderDict[time_Of_this_Candle]["low"]                 = float(x["mid"]['l'])
                innderDict[time_Of_this_Candle]["heikin_ashi_close"]   = 0.25 * (float(x["mid"]['o']) + float(x["mid"]['c']) + float(x["mid"]['l']) + float(x["mid"]['h']))
                innderDict[time_Of_this_Candle]["volume"]              = int(x["volume"])
                innderDict[time_Of_this_Candle]["time"]                = (time_Of_this_Candle - timedelta(hours=4)).time() 
                innderDict[time_Of_this_Candle]['estTime']             = innderDict[time_Of_this_Candle]["time"] #TODO this should probably be made more correctly This may effect stats from my analysis in the end
                innderDict[time_Of_this_Candle]['timeOnly']            = innderDict[time_Of_this_Candle]["time"] #TODO this should probably be made more correctly

        return innderDict


""" This Section is setting up the Pandas dataframes
    Production mode uses APIs from exchanges
    ProdictionMode == False, Means we are using
    csv data provided
    Also currencies_for_pandas      = ["GBPUSD","EURUSD"]
    need to be hardcoded correctly
""" 
def init_pandasDf_henksi_multiple_time_frames_but_trades_made_on_time_frame(
      productionMod, 
      isCsv,
      currencys_,
      secretInfo = None):


    #WHAT THE FUCK?
    # if not productionMod :  currencys_      = ["GBPUSD","EURUSD"] #This is confusing as shit, why do I have this?
    # if productionMod : currencys_ = optimizedValues.keys() 
    
    #IniitDF # This return a empty JSON if not
    if not isCsv:
       dict_of_currency_to_json_response_from_api_resquest = first_call_to_get_data_from_exchange(
          productionMod, 
          currencys_,
          secretInfo)
    else : 
       dict_of_currency_to_json_response_from_api_resquest = {}
    #Actuall I think this is good
    #Even for multiCurrency time frames
    #It is a good move to move this to 
    dict_of_currency_to_pandas_df     = setup_pandas_df_forall_currencies(
      (not isCsv), 
      dict_of_currency_to_json_response_from_api_resquest,
      currencys_)
    
    
    return dict_of_currency_to_pandas_df

def init_stateMap_henksi_multiple_time_frames_but_trades_made_on_time_frame(
      debugMode, 
      dict_of_currency_to_pandas_df_, 
      curruenciesToUse
      ):
    
    # Reading from json file
    with open('Strategy_Setup/timeMapAndOptimizedValuesV2.json', 'r') as openfile: optimizedValuesNew = json.load(openfile)
    dict_of_state_maps      = createStateMap_for_only_correlatred_trades(optimizedValuesNew, curruenciesToUse)            
    for currency, statemp in dict_of_state_maps.items(): 
      
      if  currency in curruenciesToUse:
        if debugMode : 
          print(currency)#, dict_of_currency_to_pandas_df_)
          print("statemp", statemp)
          print( dict_of_currency_to_pandas_df_.keys())
          print("dict_of_currency_to_pandas_df_[currency]", dict_of_currency_to_pandas_df_[currency])
        dict_of_state_maps[currency] = make_current_state(dict_of_currency_to_pandas_df_[currency],  statemp)
    return dict_of_state_maps
