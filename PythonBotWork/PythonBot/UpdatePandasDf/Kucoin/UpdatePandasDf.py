
from collections import defaultdict
import requests
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, time
from urllib.error import HTTPError

#Wow after looking at this
#Why the fuck is onada so ugly?

#this function should go into the update_pandas_ or something, not here
def check_if_new_pandas_info_kucoin(
        old_Df, new_Df):
    was_update= False
    for time__, d_of_currenc_to_d_of_info in old_Df.items():
        for currenc_, _ in d_of_currenc_to_d_of_info.items():
            
            if old_Df[time__][currenc_]['time'].tail(1) == new_Df[time__][currenc_]['time'].tail(1): pass
            else: 
                df = pd.concat([old_Df[time__][currenc_]['time'], new_Df[time__][currenc_]['time'] ])
                df = df.reset_index(drop=True)
                old_Df[time__][currenc_]['time']  = df
                was_update = True

    return (old_Df, was_update)


# def update_state_map(
#         old_Df, new_Df):
#     was_update= False
#     for time__, d_of_currenc_to_d_of_info in old_Df.items():
#         for currenc_, _ in d_of_currenc_to_d_of_info.items():
            
#             if old_Df[time__][currenc_]['time'].tail(1) == new_Df[time__][currenc_]['time'].tail(1): pass
#             else: 
#                 df = pd.concat([old_Df[time__][currenc_]['time'], new_Df[time__][currenc_]['time'] ])
#                 df = df.reset_index(drop=True)
#                 old_Df[time__][currenc_]['time']  = df
#                 was_update = True

#     return (old_Df, was_update)