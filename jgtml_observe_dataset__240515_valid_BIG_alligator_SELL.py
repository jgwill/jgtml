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
t = "D1"
t = "H6"

ip="AOAC"
ip ="JTLAOAC"
showpc = True

#savecsvpath='/data/src/fxpy/'
#savecsvpath='/w/indicators/exports/'
savecsvpath='./output'

ifn=i.replace("/","-")
idsfilepath=f"/var/lib/jgt/full/data/targets/mx/{ifn}_{t}.csv"
#df = pd.read_csv(idsfilepath)
df=None
try:
    df = jtc.readMXFile(i,t)
except:
    pass

mfi_flag=True
balligator_flag=True
regenerate_cds = True
use_fresh=True
#%pip install -U jgtpy

#set DF to None if column 'mfi' is not present
if df is not None and 'mfi' not in df.columns:
    df = None

if df is None:
    df, sel1, sel2 = jtc.pto_target_calculation(i,t,
                                                mfi_flag=mfi_flag,balligator_flag=balligator_flag,
                                                regenerate_cds=regenerate_cds,
                                                use_fresh=use_fresh)

l=len(df)
print(df.tail(1))
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
sel_columns = ['High','Low','bjaw','blips','bteeth','jaw','teeth','lips','fdbs','target', 'vaosc', 'vaoc']
dfo = df[sel_columns]


# %%
print(dfo.columns)

# %%
# Select row where target is not 0
dfo = dfo[dfo['target'] != 0] 
#dfoprofit = dfo[dfo['target'] > 0] 
# %%
dfo

# %%
dfosell = dfo[sel_columns].copy()
#dfosell = dfo[['fdbs','target', 'vaoc']].copy()

dfosell = dfosell[dfosell['fdbs'] != 0].copy()


#dfosell = dfosell[dfosell['fdbs'] != 0] 



# dfo = dfo[dfo['target'] != 0] #Where target is not 0
# %%
dfosell.tail(40)
# %%
all_sell_signal_count = len(dfosell)

all_sell_signal_sum=dfosell['target'].sum()

print("count_sell:",all_sell_signal_count," sum0:",all_sell_signal_sum)

# %%
#Remove invalid signal when column High < lips
#@STCGoal Valid Signals are bellow the lips and teeth 
not_in_lips_teeth = dfosell[dfosell['Low'] > dfosell['lips']].copy()
not_in_lips_teeth = not_in_lips_teeth[not_in_lips_teeth['Low'] > not_in_lips_teeth['teeth']]
not_in_lips_teeth_count = len(not_in_lips_teeth)
not_in_lips_teeth_sum=not_in_lips_teeth['target'].sum()


print("not_in_lips_teeth:",not_in_lips_teeth_count," sum:",not_in_lips_teeth_sum)


# %%
not_in_lips_teeth.tail(40)

# %%
#Remove invalid signal when column High < lips
#@STCGoal Valid Signals when mouth is open
mouth_is_open = not_in_lips_teeth[not_in_lips_teeth['jaw'] < not_in_lips_teeth['teeth']].copy()
mouth_is_open = mouth_is_open[mouth_is_open['teeth'] < mouth_is_open['lips']]
mouth_is_open = mouth_is_open[mouth_is_open['jaw'] < mouth_is_open['lips']]
mouth_is_open_count = len(mouth_is_open)
mouth_is_open_sum=mouth_is_open['target'].sum()


print("count_sell3:",mouth_is_open_count," sum3:",mouth_is_open_sum)

# %%
mouth_is_open.tail(40)
# %%
print("count_sell (no validation):",all_sell_signal_count," sum0:",all_sell_signal_sum)
print("count_sell2 not_in_lips_teeth:",not_in_lips_teeth_count," sum2:",not_in_lips_teeth_sum)
print("count_sell3 mouth_is_open:",mouth_is_open_count," sum3:",mouth_is_open_sum)






# # %%
# dfosell_vaoc_min_bar.tail(20)
# %%

# %%

result_of_this_analysis = """
Best Validation : not in lips and teeth

NEXT STEP : 

* Larger Timeframe insights.
"""


#@STCGoal  Eval Big Mouth 
# %%  BIG ALLIGATOR SELL - Eval Low is Bellow Big Teeth

sig_is_in_bteeth = not_in_lips_teeth[
    not_in_lips_teeth['Low'] > not_in_lips_teeth['bteeth']
    ].copy()

sig_is_in_bteeth_count = len(sig_is_in_bteeth)
sig_is_in_bteeth_sum=sig_is_in_bteeth['target'].sum()

# %%
sig_is_in_bteeth.tail(40)

print("sig_is_in_bteeth:",sig_is_in_bteeth_count," sum:",sig_is_in_bteeth_sum)




# %%  BIG ALLIGATOR SELL - Eval Low is Above Big Lips and Big Mouth is Open

big_m_open_in_bteeth = not_in_lips_teeth[
    not_in_lips_teeth['Low'] > not_in_lips_teeth['bteeth']
    ].copy()

big_m_open_in_bteeth = big_m_open_in_bteeth[  #@a The Big Mouth Is Open
    big_m_open_in_bteeth['blips'] < big_m_open_in_bteeth['bteeth']
    ]
big_m_open_in_bteeth = big_m_open_in_bteeth[  #@a The Big Mouth Is Open
    big_m_open_in_bteeth['bteeth'] < big_m_open_in_bteeth['bjaw']
    ]                        
                                       
big_m_open_in_bteeth_count = len(big_m_open_in_bteeth)
big_m_open_in_bteeth_sum=big_m_open_in_bteeth['target'].sum()

# %%
big_m_open_in_bteeth.tail(40)

print("count_sell2s2 Low is Above Big Teeth and Big Mouth is Open:",big_m_open_in_bteeth_count," sum2s2:",big_m_open_in_bteeth_sum)


# %%  BIG ALLIGATOR SELL - Eval Low is Above Big Lips and Big Mouth is Open

sig_in_blips_bmouth_is_open = not_in_lips_teeth[
    not_in_lips_teeth['Low'] < not_in_lips_teeth['blips']
    ].copy()

# the BMouth is Openned
sig_in_blips_bmouth_is_open = sig_in_blips_bmouth_is_open[
    sig_in_blips_bmouth_is_open['blips'] < sig_in_blips_bmouth_is_open['bteeth']
    ]
sig_in_blips_bmouth_is_open = sig_in_blips_bmouth_is_open[
    sig_in_blips_bmouth_is_open['bteeth'] < sig_in_blips_bmouth_is_open['bjaw']
    ]
                                                                    
sig_in_blips_bmouth_is_open_count = len(sig_in_blips_bmouth_is_open)
sig_in_blips_bmouth_is_open_sum=sig_in_blips_bmouth_is_open['target'].sum()

# %%
sig_in_blips_bmouth_is_open.tail(40)

print("count_sell2s2 Low is Above Big Lips and Big Mouth is Open:",sig_in_blips_bmouth_is_open_count," sum2s2:",sig_in_blips_bmouth_is_open_sum)





# %%
def print_res(nb_entry, tsum, title):
    per_trade=round(tsum/nb_entry,2)
    print(f"{i}_{t} pt:{per_trade} t:{nb_entry} sum:{round(tsum,2)} title:{title}")

# %%
print("==============================================================")
print_res(all_sell_signal_count,all_sell_signal_sum,"All Sell Signal - no filtering")
print_res(mouth_is_open_count,mouth_is_open_sum,"mouth_is_open")
print("==============================================================")
print_res(not_in_lips_teeth_count,not_in_lips_teeth_sum,"not_in_lips_teeth")
print("==============================================================")
print_res(sig_is_in_bteeth_count,sig_is_in_bteeth_sum,"sig_is_in_bteeth_sum")
print_res(sig_in_blips_bmouth_is_open_count,sig_in_blips_bmouth_is_open_sum,"sig_in_blips_bmouth_is_open")
#pt:32.42 t:132 sum:4279.999999999999 title:count_sell2s2 Low is Above Big Lips and Big Mouth is Open
print_res(big_m_open_in_bteeth_count,big_m_open_in_bteeth_sum,"big_m_open_in_bteeth_sum")
print("==============================================================")


#@STCIssue SPX500 D1, big_m_open_in_bteeth_sum has an interesting value when the Signal bar is in the big mouth
#pt:83.2 t:99 sum:8237.0 title:big_m_open_in_bteeth_sum
# %%