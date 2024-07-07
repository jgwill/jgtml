import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtutils.jgtconstants import MFI_VAL,MFI_SIGNAL,VOLUME,FDB_TARGET as TARGET
#from jgtpy import mfihelper,JGTCDSSvc as cdssvc
import anhelper as anh
import mxhelper
import mxconstants
import jtc
import pandas as pd


#@STCGoal We Have TTF Data with Lags for the pattern 'ttf_mfis_ao_2407a'
#@STCIssue How are created the TTF ?  How to create them with the lags and smaller Datasets (we dont need full)?

from jgtml.ptottf import read_ttf_csv
#from jgtml import anhelper

from jgtml.mfihelper2 import column_mfi_str_in_dataframe_to_id as convert_mfi_columns_from_str_to_id

from jgtml.mxhelper import _mfi_str_add_lag_as_int as add_mfi_lagging_feature_to_ttfdf

def _pto_get_dataset_we_need_in_here__2407060929(i,t,lag_period=1, total_lagging_periods=5,dropna=True, use_full=True,columns_to_keep=None):
  #Read Data
  df=read_ttf_csv(i, t, use_full=use_full)
  #Convert the MFI columns from str to id before we add lags
  df=convert_mfi_columns_from_str_to_id(df,t, inplace=True)
  #add lags
  df=add_mfi_lagging_feature_to_ttfdf(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,inplace=True)
  if dropna:
    df.dropna(inplace=True)
  if columns_to_keep:
    df=df[columns_to_keep]
  #columns_to_add_lags_to = mxhelper.get_mfi_features_column_list_by_timeframe(t)
  #ttfdf=anhelper.add_lagging_columns(ttfdf, columns_to_add_lags_to)
  return df
  

def create_pattern_dataset__ttf_mfis_ao_2407a(i,t,lag_period=1, total_lagging_periods=5,drop_columns_arr = ['BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'AskOpen', 'AskHigh','AskLow', 'AskClose', 'fh13', 'fl13', 'fh21', 'fl21', 'fh34', 'fl34', 'fh55','fl55','price_peak_above', 'price_peak_bellow', 'ao_peak_above','ao_peak_bellow'],dropna_volume=True):
  
  df=_read_mx_and_prep_02(i,t,drop_columns_arr,dropna_volume)
  _mfi_str_add_lag_as_int(df,t,lag_period, total_lagging_periods)
  return df
