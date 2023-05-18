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


def getBearAndAccount():    
    with open('../bearTokenAndAccountInfo.json', 'r') as openfile:
        # Reading from json file
        oauthInfo = json.load(openfile)
    
    bearerTokenOanda = oauthInfo["bearer"]
    accountNumOanda  = oauthInfo["account"] 

    return (bearerTokenOanda, accountNumOanda)


