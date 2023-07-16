from datetime import datetime, timedelta, time
from   collections import defaultdict
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from   inspect import currentframe, getframeinfo
import requests
from   time import sleep


from pandas_datareader import data
import mplfinance as mpf





def test_show_candle_chart(strategies):
    for strategy in strategies.keys():
      df_whatever = strategies[strategy]["pandas_df"]
      for time_frame_, dict_of_currenC_to_pandasdf in df_whatever.items():
        number_of_currenC_pandas = len(list(dict_of_currenC_to_pandasdf.keys()))
        if number_of_currenC_pandas == 0: pass #this means are no pandas dfs, related to those time frames.
        else: 

          
          fig, axs = plt.subplots(number_of_currenC_pandas, 1, figsize=(10, 8))

          for i, (currenC, pandaIsDTF) in enumerate(dict_of_currenC_to_pandasdf.items()):
          # for currenC, pandaIsDTF in  dict_of_currenC_to_pandasdf.items():
            df_bitcoin = pandaIsDTF
            #check if time needs to be converted to a datetime object then
            # Convert the 'Date' column to datetime if it is not already in datetime format
            if df_bitcoin['time'].dtype == 'object' and df_bitcoin['time'].apply(lambda x: isinstance(x, time)).all():
                df_bitcoin['Date'] = df_bitcoin['time']
                #df_bitcoin.index = pd.to_datetime(df_bitcoin.index)
                print("wait, why isn't this a dateTime instance?", type(df_bitcoin['time'].tail(1)), df_bitcoin['time'].tail(1 ) )
                df_bitcoin.set_index('Date', inplace=True)
                

            else:
                df_bitcoin['Date'] = pd.to_datetime(df_bitcoin['time'])
                print("The index is a DatetimeIndex.")
                df_bitcoin.set_index('Date', inplace=True)
                df_bitcoin.index = pd.to_datetime(df_bitcoin.index)
                
            
                # Set the 'Date' column as the index of the DataFrame
                        
            if isinstance(df_bitcoin.index, pd.DatetimeIndex):
                
                try: mpf.plot(df_bitcoin, type='candle', style='yahoo', title= str(currenC), mav=(20), ax=axs[i])
                except Exception : print("failed to create map")
                else: print("Continue the proccess....")
            
            else:
                print("The index is not a DatetimeIndex.")

        # Adjust spacing between subplots
          plt.tight_layout()

        # Show the plot
          try: plt.show()

          except Exception: print("Couldn't get the plot to show")

          else: print("No exception occurred.")