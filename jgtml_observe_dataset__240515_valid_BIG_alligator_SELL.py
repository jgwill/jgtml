#%% Imports 

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd


import os

import numpy as np
import pandas as pd
try:
    from jgtpy import JGTCDS as cds
except:
    print("pip install -U jgtpy")

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
t = "H6"
t = "H1"
t = "D1"
t = "H4"




# FLAGS for the PROCESS we might want to configure or read from ENV
force_regenerate_mxfiles=True
mfi_flag=True
balligator_flag=True
regenerate_cds = True
use_fresh=True

# OUTPUTS Files
jgtdroot_default="/b/Dropbox/jgt" #$jgtdroot
jgtdroot=os.getenv("jgtdroot",jgtdroot_default)
#result_drop_base_default="/b/Dropbox/jgt/drop" #$jgtdroot
result_drop_base=os.path.join(jgtdroot, "drop")

# result_source_dataset_archive= result_drop_base + "/data/arch/jgtml_240516"
result_source_dataset_archive= os.path.join(result_drop_base, "data", "arch", "jgtml_240516")
# result_file_base=result_drop_base+"/jgtml_observe_dataset__240515_valid_BIG_alligator_SELL.result"
result_file_basename = "jgtml_observe_dataset__240515_valid_BIG_alligator_SELL.result"

# Columns to select
sel_columns_sell = ['High','Low','bjaw','blips','bteeth','jaw','teeth','lips','fdbs','target', 'vaosc', 'vaoc']
sel_columns_buy = ['High','Low','bjaw','blips','bteeth','jaw','teeth','lips','fdbb','target', 'vaobc', 'vaoc']

jgtpy_data_full_var_name = "JGTPY_DATA_FULL"

bs="S" # This prototype is for SELL signals only, we can extend it to BUY signals later
if bs=="S":
    sel_columns = sel_columns_sell
else:
    if bs=="B":
        sel_columns = sel_columns_buy

#if __main__
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some JGTML.')
    parser.add_argument('-i','--instrument', type=str, default='SPX500', help='Instrument')
    parser.add_argument('-t','--timeframe', type=str, default='D1', help='Timeframe')
    args = parser.parse_args()
    i = args.instrument
    t = args.timeframe
    print(f"i:{i} t:{t}")
    

result_file_base = os.path.join(result_drop_base, result_file_basename)

result_file_md=result_file_base + ".md"
result_file_csv=result_file_base + ".csv"

os.makedirs(result_source_dataset_archive,exist_ok=True)



ifn=i.replace("/","-")
data_dir = os.getenv(jgtpy_data_full_var_name)
idsfilepath = os.path.join(data_dir, "targets", "mx", f"{ifn}_{t}.csv")
#df = pd.read_csv(idsfilepath)
df=None
try:
    if not force_regenerate_mxfiles:
        df = jtc.readMXFile(i,t)
except:
    pass

#%pip install -U jgtpy

#set DF to None if column 'mfi' is not present
if df is not None and 'mfi' not in df.columns:
    df = None

if df is None:
    df, sel1, sel2 = jtc.pto_target_calculation(i,t,
                                                mfi_flag=mfi_flag,balligator_flag=balligator_flag,
                                                regenerate_cds=regenerate_cds,
                                                use_fresh=use_fresh)

#%%
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

dfo = df[sel_columns]


# %%
print(dfo.columns)

# %%
# Select row where target is not 0
dfo = dfo[dfo['target'] != 0] 
#dfoprofit = dfo[dfo['target'] > 0] 
# %%
dfo


#%% Direction
direction = bs
# %%
dfo_context = dfo[sel_columns].copy()
#dfosell = dfo[['fdbs','target', 'vaoc']].copy()

fdb_context_colname = 'fdbs'
if bs=="B":
    fdb_context_colname = 'fdbb'
dfo_context = dfo_context[dfo_context[fdb_context_colname] != 0].copy()


#dfosell = dfosell[dfosell['fdbs'] != 0] 



# dfo = dfo[dfo['target'] != 0] #Where target is not 0
# %%
dfo_context.tail(40)
# %%
all_context_signal_count = len(dfo_context)

target_colname = 'target'
all_sell_signal_sum=dfo_context[target_colname].sum()

print("count:",all_context_signal_count," sum0:",all_sell_signal_sum)

# %%
#Remove invalid signal when column High < lips
#@STCGoal Valid Signals are bellow the lips and teeth 
if bs=="S":
    not_in_lips_teeth = dfo_context[dfo_context['Low'] > dfo_context['lips']].copy()
    not_in_lips_teeth = not_in_lips_teeth[not_in_lips_teeth['Low'] > not_in_lips_teeth['teeth']]
else:
    not_in_lips_teeth = dfo_context[dfo_context['High'] < dfo_context['lips']].copy()
    not_in_lips_teeth = not_in_lips_teeth[not_in_lips_teeth['High'] < not_in_lips_teeth['teeth']]

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


print("count3:",mouth_is_open_count," sum3:",mouth_is_open_sum)

# %%
mouth_is_open.tail(40)
# %%
print("count (no validation):",all_context_signal_count," sum0:",all_sell_signal_sum)
print("count_2 not_in_lips_teeth:",not_in_lips_teeth_count," sum2:",not_in_lips_teeth_sum)
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


def write_to_result_csv(i,t,direction,nb_entry, tsum, title,_df=None):
    per_trade=round(tsum/nb_entry,2)
    if direction == "sell" or direction=="Sell" or direction=="SELL":direction="S"
    if direction == "buy" or direction=="Buy" or direction=="BUY":direction="B"
    
    #per_trade="per_trade"
    with open(result_file_csv, "a") as file_object:
        tsum_rounded = round(tsum,2)
        file_object.write(f"{i},{t},{direction},{per_trade},{nb_entry},{tsum_rounded},{title}\n")
    if _df is not None:
        save_df_archives(i, t, title, _df)

def save_df_archives(i, t, title, _df,quiet=True):
    ifn = i.replace("/","-")
    csv_fn = f"{result_source_dataset_archive}/{ifn}_{t}_{title}.csv"
    if not quiet:
        print("Writing CSV to file:",csv_fn)
    _df.to_csv(csv_fn)

#save the original df
save_df_archives(i, t, "original", df)
#write_to_result_csv("instrument","timeframe","nb_entry","tsum","title")

def write_to_result_md(entry_line):
    with open(result_file_md, "a") as file_object:
        file_object.write(f"{entry_line}\n")

def print_res(i,t,direction,nb_entry, tsum, title,_df=None):
    per_trade=round(tsum/nb_entry,2)
    tsum_rounded = round(tsum,2)
    entry_line = f"{i}_{t} {direction} pt:{per_trade} t:{nb_entry} sum:{tsum_rounded} title:{title}"
    print(entry_line)
    write_to_result_md(entry_line)
    write_to_result_csv(i,t,direction,nb_entry, tsum, title,_df)
# %%

write_to_result_md("  ")
write_to_result_md("----")
write_to_result_md("  ")
write_to_result_md("==============================================================")
print_res(i,t,direction,all_context_signal_count,all_sell_signal_sum,"all_sell_sig",dfo_context)
print_res(i,t,direction,mouth_is_open_count,mouth_is_open_sum,"mouth_is_open",mouth_is_open)
write_to_result_md("==============================================================")
print_res(i,t,direction,not_in_lips_teeth_count,not_in_lips_teeth_sum,"not_in_lips_teeth",not_in_lips_teeth)
write_to_result_md("==============================================================")
print_res(i,t,direction,sig_is_in_bteeth_count,sig_is_in_bteeth_sum,"sig_is_in_bteeth_sum",sig_is_in_bteeth)
print_res(i,t,direction,sig_in_blips_bmouth_is_open_count,sig_in_blips_bmouth_is_open_sum,"sig_in_blips_bmouth_is_open",sig_in_blips_bmouth_is_open)
#pt:32.42 t:132 sum:4279.999999999999 title:count_sell2s2 Low is Above Big Lips and Big Mouth is Open
print_res(i,t,direction,big_m_open_in_bteeth_count,big_m_open_in_bteeth_sum,"big_m_open_in_bteeth_sum",big_m_open_in_bteeth)
write_to_result_md("==============================================================")


#@STCIssue SPX500 D1, big_m_open_in_bteeth_sum has an interesting value when the Signal bar is in the big mouth
#pt:83.2 t:99 sum:8237.0 title:big_m_open_in_bteeth_sum
# %%