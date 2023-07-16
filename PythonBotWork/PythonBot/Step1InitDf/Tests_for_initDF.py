
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


from InitDf_only_correlated_trade_at_once import *




currenciesToTest = ["EUR_USD", "GBP_USD", "AUD_USD", "USD_CHF"]
df = getPandasFromCSVFiles(currenciesToTest, "../")
# print(os.listdir(os.curdir))
# print("----- df print out\n", df)
# print("--------------------")
# for k, v in df.items():
#     print("\tkey:", k, "value shape", v.shape)
#     print(v.iloc[1]['time'])

if len(list(df.keys())) != len(currenciesToTest):
    raise Exception(
        "Dicitonary of Pandas DF should be size of currencies used")

getShapeOfAllDfs =  [ x.shape for x in list((df.values()))]
if len(getShapeOfAllDfs) >0  and not getShapeOfAllDfs.count(getShapeOfAllDfs[0]) == len(getShapeOfAllDfs):
    raise Exception(
        "Pandas dfs should all be the same shape!!!, nut are not....")

print("passes df init tests for csv")
    
