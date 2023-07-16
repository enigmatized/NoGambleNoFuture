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

def getCandles_aka_callToUpdateInfo(currency, 
                                    count = "3", 
                                    granularity = "H4", #TODO add logic to decide M15/M30/H1/H4
                                    bearerToken = None, 
                                    accountNum = None):
    
    #Just throw an error if no BearerToken in provided
    if bearerToken == None or accountNum == None : raise ValueError('Calling the APIs without token/account info is a very bad thing, are you really prepared for this?')
    
    
    #if type(granularity) == int : #TODO probably a good idea to add this to currency
    d = {15: "M15", 30: "M30", 60:"H1", 120 : "H2", 240: "H4"}
    granularity = d[int(re.search(r'\d+', granularity).group())]


    try:
        r = requests.get('https://api-fxtrade.oanda.com/v3/instruments/'+currency +'/candles?count='+ count +'&price=M&granularity='+ granularity,
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

def firstCallToInitState(currency, time_frame, secretInfo): 
  #Special case to start the state,
  #This should not return a tuple object and I call it here
  #I should have a check or throw an error
  #If this is bad then the entire project is bad
  print("\ntimeframe\n", time_frame, currency) #TODO delete
  (result, was_a_success) = getCandles_aka_callToUpdateInfo(
     currency,
     "80", #Number of candles
     time_frame,
     secretInfo["bearerTokenOanda"],
     secretInfo["accountNumOanda"])
  if was_a_success: return result
  else: raise Exception("Error in firstCallToInitState, to init the ondada pandas df server failed to get into to finish proccess")



""" """
def first_call_to_get_data_from_exchange(productoinMod, currencys_, time_frame, secretInfo, isDebug_ = False):
  if productoinMod:
    resDict = {}
    for currency_pair in currencys_: 
       if isDebug_: print("currenc with entire dict", currency_pair,resDict )
       resDict[currency_pair] = firstCallToInitState(currency_pair, time_frame, secretInfo)
       if isDebug_:  print("currenc", currency_pair,resDict[currency_pair] )
    return resDict
  else : 
    #TODO implemnt your Test
    return {}


def setup_pandas_df_forall_currencies(productoinMod, diction, currencies_if_not_production, ifDebug_ = False):
  if ifDebug_ : print("In setup_pandas_df_forall_currencies, \tthe data structure named diction: ", diction, "\n\tand currencies_if_not_production", currencies_if_not_production)
  
  if productoinMod:
    resD = defaultdict(dict)
    for time_frame, dict_currency_to_api_responses in diction.items(): 
      for currency, json_response_from_api_resquest in dict_currency_to_api_responses.items(): 
       resD[time_frame][currency] = createPandasDfFromAPI(json_response_from_api_resquest)
    return resD
       
  else : return getPandasFromCSVFiles(currencies_if_not_production)  #TODO this will have to change because I am changing the data structure for pandas

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

  dict_time_to_json_info_canldes     = prep_json_from_API_for_pandas(json_of_currency)

  mainDf                             = pd.DataFrame(dict_time_to_json_info_canldes).T
  mainDf['heikin_ashi_open']  = 0.5 *( mainDf['close'].shift(1) +mainDf['open'].shift(1) ) 
  
  #Get rid of the first value that is NA as a result of the above operation
  mainDf       = mainDf.tail(-1) 

  return mainDf


#TODO there should be a unit test for this
def prep_json_from_API_for_pandas(json_Instrument_Info):
        innderDict = defaultdict(dict)
        
        inst    = json_Instrument_Info['instrument']
        grans   = json_Instrument_Info['granularity']
        candles = json_Instrument_Info['candles']
        #time_to_subtract = datetime.strptime("4:00:00", "%H:%M:%S")

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
      list_of_currnec,
      list_of_time_frames = [],
      secretInfo = None):
    #This is a special function in the sense it creates the pandas df from scratch
    #AKA the beginning state of the pandas

    #THIS IS A TWO PART FUNCTION
    #FIRST CALL THE API
    #THEN CREATE THE PANDAS DF FROM
    #THE API JSON

    if isCsv: 
      dict_of_currency_to_json_response_from_api_resquest = {}
    else : 

      d_time_frame_currency_json = defaultdict(dict)
      for time_frame in list_of_time_frames:


        d_time_frame_currency_json[time_frame]   = first_call_to_get_data_from_exchange(
            productionMod,
            list_of_currnec,
            time_frame, 
            secretInfo)
      
    dict_of_currency_to_pandas_df     = setup_pandas_df_forall_currencies(
      productionMod, 
      d_time_frame_currency_json,
      list_of_currnec)

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
