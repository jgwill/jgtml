import pandas as pd
from jgtutils.jgtconstants import nonTradingZoneColor,sellingZoneColor,buyingZoneColor,ZCOL,ZONE_INT

from jgtml import anhelper

def zonecolor_str_to_id(zcol_str:str):
    if zcol_str == nonTradingZoneColor:
        return 0
    elif zcol_str == sellingZoneColor:
        return -1
    elif zcol_str == buyingZoneColor:
        return 1
    else:
        return 0
def zoneint_to_str(zint:int):
    if zint == 0:
        return nonTradingZoneColor
    elif zint == -1:
        return sellingZoneColor
    elif zint == 1:
        return buyingZoneColor
    else:
        return nonTradingZoneColor

def get_zone_columns_list(t:str):
    """
    Get the list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the list of ZONE features for.
    
    Returns:
    list: The list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    """
    
    zcol_ctx_selected_columns = [ZCOL+'_M1',ZCOL+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      zcol_ctx_selected_columns.append(ZCOL+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(ZCOL+'_H4')
        
    if t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(ZCOL+'_H1')
    
    if t=='m5':
        zcol_ctx_selected_columns.append(ZCOL+'_m15')
        
    zcol_ctx_selected_columns.append(ZCOL)
    return zcol_ctx_selected_columns
  
def column_zone_str_in_dataframe_to_id(df:pd.DataFrame,t:str,inplace=False):
    """
    Convert the ZONE columns from str to id in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The dataframe to convert the ZONE columns from str to id.
    t (str): The timeframe to convert the ZONE columns from str to id.
    inplace (bool): If True, the conversion is done in place. If False, a copy of the dataframe is returned with the conversion done.
    
    Returns:
    pd.DataFrame: The dataframe with the ZONE columns converted from str to id.
    
    """
    if not inplace:
        df = df.copy()
    zcol_features_columns_list = get_zone_columns_list(t)
    for col_name in zcol_features_columns_list:
        df[col_name] = df[col_name].apply(lambda x: int(zonecolor_str_to_id(x)))
          #zonecolor_str_to_id)
    return df

def _zoneint_add_lagging_feature(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True):
    if not inplace:
        df = df.copy()
    columns_to_add_lags_to = get_zone_columns_list(t)
    columns_to_add_lags_to.append(ZCOL) #We want a lag for the current TF
    anhelper.add_lagging_columns(df, columns_to_add_lags_to, lag_period, total_lagging_periods, out_lag_midfix_str)
    for col in columns_to_add_lags_to:#@STCIssue Isn't that done already ???  Or it thinks they are Double !!!!
        for j in range(1, total_lagging_periods + 1):
            df[f'{col}{out_lag_midfix_str}{j}']=df[f'{col}{out_lag_midfix_str}{j}'].astype(int)
    return df
    

def wf_mk_zone_ready_dataset__240708(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True):
    if not inplace:
        df = df.copy()
    column_zone_str_in_dataframe_to_id(df,t,inplace=True)
    _zoneint_add_lagging_feature(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,out_lag_midfix_str=out_lag_midfix_str,inplace=True)
    return df