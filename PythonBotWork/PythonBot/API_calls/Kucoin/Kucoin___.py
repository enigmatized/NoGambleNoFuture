
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

from kucoin_futures.client import Market
from kucoin_futures.client import Trade

# if "API" in str(os.getcwd()): 
#     from kucoin_futures.client import Market
#     from kucoin_futures.client import Trade
# elif "May_Bot_2023/May_Bot_2023_Currency_trading" in str(os.getcwd()):
#     print(str(os.getcwd()))
#     from API_calls.Kucoin.kucoin_futures.client import Market
#     from API_calls.Kucoin.kucoin_futures.client import Trade
# else: raise Exception("Import failed for your kucoin_futures_library, working directory doesn't work, are you running this in a forgein place?")

def init_pandas_df_kucoin(
      secretInfo = None,
      productionMod = False, 
      isCsv = False,
      debugMode = False,
      list_of_currnec = [],
      pandasDf = None,
      list_of_time_frames = [],
      isAnUpdate_and_not_init = False,
      ):
    
                #     secretInfo,    #For bearer Token and account info for Oanada
                # productoinMode, #Decides to use API 
                # isCsv,          #Decides to use csv
                # debugMode,      #Add print/logging statements
                # strategies[strategy_name]["currencies_in_this_stratgey"],  #Not sure why this is needed
                # strategies[strategy_name]["pandas_df"],
                # strategies[strategy_name]["times_frame_this_stratgey_is_focused_on"] #This shouldn't be needed, this should be filtered out in the future
                # )     
    
    result_dict_currenc_pandasDf = defaultdict(dict)
    client = Market()

    if isAnUpdate_and_not_init: was_there_an_update = False


    for time_ in list_of_time_frames:
        for currenc in list_of_currnec:
            
            #I think putting this try here, could causes errors down the road
            try:
                #Use library to get futures market data
                api_response = client.get_kline_data(currenc, time_)
                #add Hesnki heikin_ashi_close
                for x in api_response: x.append( 0.25 * (float(x[1]) + float(x[2]) + float(x[3]) + float(x[4]) ))
                
                #Make into pandas df
                new_df = pd.DataFrame(api_response)
                new_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'heikin_ashi_close']

                new_df['estTime']  = new_df['time'].apply(lambda x : datetime.utcfromtimestamp(int(x/1000)).strftime('%Y-%m-%d %H:%M:%S'))
                new_df['heikin_ashi_open']  = 0.5 *( new_df['close'].shift(1) + new_df['open'].shift(1) )
        
                new_df['timeOnly'] =new_df['estTime'].apply(lambda date_string : (datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")).strftime("%H:%M:%S"))
                new_df   = new_df.tail(-1) #Since two rows, first row is complete, last is not
                result_dict_currenc_pandasDf[time_][currenc] = new_df
                
                if isAnUpdate_and_not_init:
                    tail_of_current = result_dict_currenc_pandasDf[time_][currenc]['time'].tail(1)
                    
                    
                    if pandasDf == None: raise ValueError("This should not happen,Pandas df should never be none and we are updating")
                    #print("WTF1 when does this start", type(tail_of_current))
                    #print("WTF2 when does this start", type(pandasDf[time_][currenc]['time']))
                    if not pandasDf[time_][currenc]['time'].tail(1).equals(tail_of_current):
                        print("THis really shouldn't happen often, that is updating and there is a change")
                        print("THis really shouldn't happen often, that is updating and there is a change" )
                        print("If this is happening a lot then you should take some time off")
                        print("Actaully inspect these pandas dfs")
                        was_there_an_update = True
            except BaseException:  # Specify the specific exception you want to catch
            # Code to handle the exception
                print("An exception occurred.!!!!.... This SHOULD NOT BE HAPPENING, looking into this")
                
                # Alternate operation or function
            else: print("No exception occurred. Continue with normal operation.")
            finally: pass

    if isAnUpdate_and_not_init: return (result_dict_currenc_pandasDf,    was_there_an_update, None   ) #Last arguement is for incomplete data, but that doesn't apply to kucoin
    else: return result_dict_currenc_pandasDf





 



def make_orders_kucoin_futures(
        price, 
        optmizedStopLossValue, 
        dirrection, 
        currency = "XBTUSDM", 
        amount = "1",
        secret_info=None):

    print("make_orders_kucoin_futures ", price, optmizedStopLossValue, dirrection, currency)
    
    #stopLossValue = price - optmizedStopLossValue if dirrection == "green" else price + optmizedStopLossValue
    stopLossValue = price - 0.005 if dirrection == "green" else price + 0.005
    buy_or_sell = "buy" if dirrection == "green" else "sell"   

    try:

        client    = Trade(key=secret_info["apiKeyi"], secret=secret_info["Secret"], passphrase=secret_info["passphrase"], is_sandbox=False, url='')
        order_res = client.create_market_order('XBTUSDM', buy_or_sell, '1', '1')
        return (order_res, True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
        print(price, optmizedStopLossValue, dirrection, currency)
    except Exception as err:
        print(f'Other error occurred in make_orders_: {err}')
    return ("", False)


def get_orders_I_am_in(secret_info):
    #TODO I should make it so I am not making these clients everytime
    #I should have the data bot, hold onto it and then refresh it as is


    try:

        client = Trade(key=secret_info["apiKeyi"], secret=secret_info["Secret"], passphrase=secret_info["passphrase"], is_sandbox=False, url='')
        kucoin_json_response = client.get_order_list()
        return (kucoin_json_response, True)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(http_err.response.text)
        print({}, False)
    except Exception as err:
        print(f'Other error occurred in make_orders_: {err}')
    return ({}, False)


#Data feed
#Once I data feed is update it triggers
#the logic to update/df
#if df update then that triggers 

#Run data feed
#Which would be a like spin a thread for each data thread?

#for x in dataFeeds: run(thread):

# def thread():
#     while True:
#         (data, True) = checkUpdate()
#         if true: check if needs pandasUpdate
#         if needsPandas


#         sleep()


# #TODO update with websockets
def get_orderbook_kucoin(
      list_of_currnec
      #productionMod, 
      #isCsv,
      #secretInfo = None,
      ):

    client = Market()

    res = defaultdict(dict)

    for currenC  in list_of_currnec: res[currenC] = client.l2_order_book(currenC)

    print("yes!")
    return res


# import inspect
# client = Market()
# lines = inspect.getsource(client.l2_order_book)
# print(lines)



# print(len(get_orderbook_kucoin(["ETHUSDTM"])))