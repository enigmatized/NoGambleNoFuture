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


#THIS SHOULD BE A PANDAS DF of one row only!!!!!
#Should make a fail statement if not then case
#Also this assume we have a time column
#Should throw an error if that isn't the case


#This slightly assumes I will not get a data mismatch
#stateMap Dict<time, Dict<Currency, Innder_state_map >>
def update_state_map_from_new_pandas_info(
        isDebug,
        isCsv, 
        dict_of_new_pandas_result, 
        stateMap, 
        lsOfCurrencues,
        indexxxxxxxxx = 0, 
        shouldBeOneRow = True):
    
    #HOw do I actually want to do this?
    #Two seperate functions, ?
    #I think so
    #if isCsv: 
        #print("dict_of_new_pandas_result.keys()", list(dict_of_new_pandas_result.values())[0] )
        #index +=1 #DO I want to make sure this is the only place index gets used?
        #sleep(60)
       
    #print("keys, should be", list(dict_of_new_pandas_result.keys()))

    #So we are iterating through the statemaps
    #By time first, but they are broken down by
    #time, then currencies in the time
    #I am realizing that I should have the statemap and pandas standardized to be the same thing
    #So I am not getting weird key errors


    #print("dict_of_new_pandas_result keys:", list(dict_of_new_pandas_result.keys()), "\ndict_of_new_pandas_result[aKey] keys:" , list(dict_of_new_pandas_result[list(dict_of_new_pandas_result.keys())[0]].keys())  )
    #print("stateMap keys:", list(stateMap.keys()), "\nstateMap[aKey] keys:" , list(stateMap[list(stateMap.keys())[0]].keys())  )

    for time_, dict_of_currenC_to_inner_state in stateMap.items():
        for currenC, inner_state_map in dict_of_currenC_to_inner_state.items():

            #Going to expeirment with commenting this out, I think it was a super simple patch
            #for csv files, but I think I should do a more proper fix,
            #now that I have difference strategies using this same function

            if isDebug:     print("What currenC in list(dict_of_new_pandas_result[time_].keys())", currenC in list(dict_of_new_pandas_result[time_].keys()), list(dict_of_new_pandas_result[time_].keys()), currenC)
            if  (currenC in lsOfCurrencues) and currenC in list(dict_of_new_pandas_result[time_].keys()): #TODO why the fuck is this here? #TODO This logic seems to be very flawed

                if isCsv: 
                    #TODO throw an error on this
                    #print("index", indexxxxxxxxx)
                    one_row_pdf = (dict_of_new_pandas_result[currenC]).iloc[[indexxxxxxxxx]]
                    if isDebug :
                        print(indexxxxxxxxx, one_row_pdf)
                        print()
                elif not isCsv:
                    if isDebug: print(dict_of_new_pandas_result.keys())
                    #WHAT THE FUCK LOGIC #TODO # dict_of_new_pandas_result[currenC].tail(1).shape[0] > 1 will always be false
                    if  shouldBeOneRow and dict_of_new_pandas_result[time_][currenC].tail(1).shape[0] > 1: print("ERRRRRRRRRRRR")
                    if shouldBeOneRow:  one_row_pdf = dict_of_new_pandas_result[time_][currenC].tail(1)
                    else : 
                        print("[time_], [currenC]", [time_], [currenC])
                        one_row_pdf = dict_of_new_pandas_result[time_][currenC]
                
                for index, row in one_row_pdf.iterrows():
                    if isDebug:
                        #if not str(row['timeOnly']) in  inner_state_map['timesToCheckForTrade'] : 
                            
                            #print(str(row['timeOnly']), "SOMETHING IS WRONG HERE?!")
                            #print() #Oh shit these times are not ligned up well.
                            #
                            #print(str(row['timeOnly']), inner_state_map['timesToCheckForTrade'])
                            #print() 
                        if not str(row['time']) in  inner_state_map['timesToCheckForTrade'] : 
                            print(str(row['time']), "SOMETHING IS WRONG HERE?!")
                    
                    
                    #NOTE WTF TODO this could cause huge issues
                    #if not isCsv: print("The below line of code could cause huge problems, test this out for live trading")
                    #Also how would this time arguement get used when looking to optimize multiuple values at a time?
                    timeToUse = row['timeOnly'] if isCsv else row['time'] 
                    
                    if str(timeToUse) in inner_state_map['timesToCheckForTrade'] :
                        
                        if isDebug: print("Do I get here in state_map_update, where I am updating a time I am looking to trade")
                        bar_candles_or_heikin_ankiki =  ('heikin_ashi_open', 'heikin_ashi_close') if True else ('open', 'close') #Change this in the future
                        
                        #BEFORE SETTING ANY VALUES IN STATE MAP
                        #These are the local values to calculate statemap
                        cur       = "green" if row[bar_candles_or_heikin_ankiki[1]] >= row[bar_candles_or_heikin_ankiki[0]] else "red"
                        lastCount = inner_state_map["count"]
                        lastColor = inner_state_map["lastColorBar"]
                        countCur  = 0 if lastColor != cur else   (lastCount + 1)
                        lastPrice = row[bar_candles_or_heikin_ankiki[1]]
                        cur_unix_time  = row['time']
                        cur_my_time    = row["timeOnly"]
                        cur_time_stamp = row["estTime"]
                        # tempToPrint = inner_state_map["lastColorBar"]
                        #if should only print if debug flag on
                        # print(k, "In make_current_state2", "cur", cur,  "lastCount", lastCount, 
                                # "stateMap[k][lastColorBar", inner_state_map['lastColorBar'], 
                                # "stateMap[k][lastColorBar] != cur ", tempToPrint != cur , 
                                # "countCur", countCur, 
                                # " (tempToPrint, countCur)" ,(tempToPrint, countCur))
                        
                        #SETTING VALUES IN STATE MAP
                        inner_state_map["lastColorBar"] =  cur
                        inner_state_map["tracker"].append( (cur , countCur, lastPrice, cur_time_stamp, cur_unix_time))
                        inner_state_map["count"] = countCur
                # Update/set Inner stateMap
                dict_of_currenC_to_inner_state[currenC] = inner_state_map
        # Update/set map of times to currencies_inner_Statemapos
        if (currenC in lsOfCurrencues) : stateMap[time_] = dict_of_currenC_to_inner_state
    return (stateMap, indexxxxxxxxx)