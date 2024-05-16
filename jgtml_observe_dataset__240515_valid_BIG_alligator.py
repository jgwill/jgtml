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

# %%
print("len(df):",len(df))

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
dfo = df[['High','Low','bteeth','blips','jaw','teeth','lips','fdbs','fdbb','target', 'vaosc', 'vaoc']]
# %%
print(dfo.columns)

# %%
# Select row where target is not 0
dfo = dfo[dfo['target'] != 0] 
#dfoprofit = dfo[dfo['target'] > 0] 
# %%
dfo

# %%
dfobuy = dfo[['High','Low','bteeth','blips','jaw','teeth','lips','fdbb','target', 'vaoc']].copy()
#dfosell = dfo[['fdbs','target', 'vaoc']].copy()

dfobuy = dfobuy[dfobuy['fdbb'] != 0].copy()



#dfosell = dfosell[dfosell['fdbs'] != 0] 



# dfo = dfo[dfo['target'] != 0] #Where target is not 0
# %%
dfobuy.tail(40)
# %%
count_buy = len(dfobuy)

sum0=dfobuy['target'].sum()

print("count_buy:",count_buy," sum0:",sum0)

# %%
#Remove invalid signal when column High < lips
#@STCGoal Valid Signals are bellow the lips and teeth 
dfobuy2_not_in_lips_teeth = dfobuy[dfobuy['High'] < dfobuy['lips']].copy()
dfobuy2_not_in_lips_teeth = dfobuy2_not_in_lips_teeth[dfobuy2_not_in_lips_teeth['High'] < dfobuy2_not_in_lips_teeth['teeth']]
count_buy2_not_in_lips_teeth = len(dfobuy2_not_in_lips_teeth)
sum2=dfobuy2_not_in_lips_teeth['target'].sum()


print("count_buy2:",count_buy2_not_in_lips_teeth," sum2:",sum2)


# %%
dfobuy2_not_in_lips_teeth.tail(40)

# %%
#Remove invalid signal when column High < lips
#@STCGoal Valid Signals when mouth is open
dfobuy3_mouth_is_open = dfobuy2_not_in_lips_teeth[dfobuy2_not_in_lips_teeth['jaw'] > dfobuy2_not_in_lips_teeth['teeth']].copy()
dfobuy3_mouth_is_open = dfobuy3_mouth_is_open[dfobuy3_mouth_is_open['teeth'] > dfobuy3_mouth_is_open['lips']]
count_buy3_mouth_is_open = len(dfobuy3_mouth_is_open)
sum3=dfobuy3_mouth_is_open['target'].sum()


print("count_buy3:",count_buy3_mouth_is_open," sum3:",sum3)

# %%
dfobuy3_mouth_is_open.tail(40)
# %%
print("count_buy (no validation):",count_buy," sum0:",sum0)
print("count_buy2 not_in_lips_teeth:",count_buy2_not_in_lips_teeth," sum2:",sum2)
print("count_buy3 mouth_is_open:",count_buy3_mouth_is_open," sum3:",sum3)


# %%
dfobuy3_mouth_is_open__profit = dfobuy3_mouth_is_open[dfobuy3_mouth_is_open['target'] > 0].copy() 

dfobuy3_mouth_is_open__profit.tail(20)




# %%

result_of_this_analysis = """
Best Validation : not in lips and teeth

NEXT STEP : 

* Larger Timeframe insights.
"""

# %%  BIG ALLIGATOR BUY, Eval Low is Bellow Big Teeth

dfobuy2b_bellow_big_teeth = dfobuy2_not_in_lips_teeth[dfobuy2_not_in_lips_teeth['Low'] > dfobuy2_not_in_lips_teeth['bteeth']].copy()

count_buy2b = len(dfobuy2b_bellow_big_teeth)
sum2b=dfobuy2b_bellow_big_teeth['target'].sum()

# %%
dfobuy2b_bellow_big_teeth.tail(40)

print("count_buy2b:",count_buy2b," sum2b:",sum2b)

# %%
def print_res(nb_entry, tsum, title):
    per_trade=round(tsum/nb_entry,2)
    print(f"pt:{per_trade} t:{nb_entry} sum:{tsum} title:{title}")
# %%
print_res(count_buy,sum0,"count_buy")
print_res(count_buy2_not_in_lips_teeth,sum2,"count_buy2_not_in_lips_teeth")
print_res(count_buy3_mouth_is_open,sum3,"count_buy3_mouth_is_open")
print_res(count_buy2b,sum2b,"count_buy2b")

# print("count_buy (no validation):",count_buy," sum0:",sum0)
# print("count_buy2 not_in_lips_teeth:",count_buy2_not_in_lips_teeth," sum2:",sum2)
# print("count_buy2b Bellow BTeeth:",count_buy2b," sum2b:",sum2b)
# print("count_buy3 mouth_is_open:",count_buy3_mouth_is_open," sum3:",sum3)
# %%