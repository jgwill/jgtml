#%% Imports 

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd



import numpy as np
import pandas as pd
from jgtpy import JGTCDS as cds
from jgtml import jtc

def crop_dataframe(df, crop_last_dt: str = None, crop_start_dt: str = None):
    if crop_last_dt is not None:
        df = df[df.index <= crop_last_dt]
    if crop_start_dt is not None:
        df = df[df.index >= crop_start_dt]
    return df


#%% Contexts 
# Contexts

i = 'GBP/USD'
i = 'SPX500'
t = "H1"
t = "H4"
t = "D1"

ip="AOAC"
ip ="JTLAOAC"
showpc = True

#savecsvpath='/data/src/fxpy/'
#savecsvpath='/w/indicators/exports/'
savecsvpath='./output'

ifn=i.replace("/","-")
idsfilepath=f"/var/lib/jgt/full/data/targets/mx/{ifn}_{t}.csv"
#df = pd.read_csv(idsfilepath)
df = jtc.readMXFile(i,t)
l=len(df)
print(df.tail(10))
#%% Columns
print(df.columns)


#%% 
"""
'Volume', 'Open', 'High', 'Low', 'Close', 'Median', 'ao', 'ac', 'jaw',
       'teeth', 'lips', 'fh', 'fl', 'fh3', 'fl3', 'fh5', 'fl5', 'fh8', 'fl8',
       'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55', 'fl55', 'fh89',
       'fl89', 'fdbb', 'fdbs', 'fdb', 'aoaz', 'aobz', 'zlc', 'zlcb', 'zlcs',
       'zcol', 'sz', 'bz', 'acs', 'acb', 'ss', 'sb', 'price_peak_above',
       'price_peak_bellow', 'ao_peak_above', 'ao_peak_bellow', 'tmax', 'tmin',
       'p', 'l', 'target', 'vaos', 'vaob', 'vaosc', 'vaobc', 'vaoc'],
      
"""
# create a dataset with only the columns we need.  'target', 'vaos', 'vaob', 'vaosc', 'vaobc', 'vaoc'
# dfo = df[['target', 'vaos', 'vaob', 'vaosc', 'vaobc', 'vaoc']]
dfo = df[['fdbs','fdbb','target', 'vaosc', 'vaobc', 'vaoc']]
# %%
print(dfo.columns)

# %%
# Select row where target is not 0
dfo = dfo[dfo['target'] != 0] 
# %%
dfo

# %%
dfobuy = dfo[['fdbb','target', 'vaobc', 'vaoc']].copy()
dfosell = dfo[['fdbs','target', 'vaosc', 'vaoc']].copy()

dfobuy = dfobuy[dfobuy['fdbb'] != 0] 

dfosell = dfosell[dfosell['fdbs'] != 0] 



# dfo = dfo[dfo['target'] != 0] #Where target is not 0
# %%
dfobuy.tail(40)
# %%
dfosell.tail(40)
# %%
