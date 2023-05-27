
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
from kucoin_futures_python_sdk.kucoin_futures import *

def init_pandas_df_kucoin(list_of_currnec, list_of_time_frames):
    
    result_dict_currenc_pandasDf = defaultdict(dict)
    client = Market()

    for time_ in list_of_time_frames:
        for currenc in list_of_currnec:
        
            
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
    
    return result_dict_currenc_pandasDf





 



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
