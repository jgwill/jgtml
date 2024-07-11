import pandas as pd
from jgtml import anhelper

from jgtutils.jgtconstants import ZCOL,ZONE_INT,ZONE_BUY_ID,ZONE_SELL_ID,ZONE_NEUTRAL_ID,ZONE_BUY_STR,ZONE_SELL_STR,ZONE_NEUTRAL_STR


def zonecolor_str_to_id(zcol_str:str):
    if zcol_str == ZONE_NEUTRAL_STR:
        return ZONE_NEUTRAL_ID
    elif zcol_str == ZONE_SELL_STR:
        return ZONE_SELL_ID
    elif zcol_str == ZONE_BUY_STR:
        return ZONE_BUY_ID
    else:
        return 0

def zoneint_to_str(zint:int):
    if zint == ZONE_NEUTRAL_ID:
        return ZONE_NEUTRAL_STR
    elif zint == ZONE_SELL_ID:
        return ZONE_SELL_STR
    elif zint == ZONE_BUY_ID:
        return ZONE_BUY_STR
    else:
        return ZONE_NEUTRAL_STR

def get_zone_columns_list(t:str,zone_colname=""):
    """
    Get the list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the list of ZONE features for.
    zone_colname (str): The name of the ZONE column to use. If not provided, the default ZCOL is used. (Planning to use ZONE_SIGNAL)
    
    Returns:
    list: The list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    """
    if zone_colname=="":
        zone_colname=ZCOL
    
    zcol_ctx_selected_columns = [zone_colname+'_M1',zone_colname+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      zcol_ctx_selected_columns.append(zone_colname+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_H4')
        
    if t=='m15' or t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_H1')
    
    if t=='m5':
        zcol_ctx_selected_columns.append(zone_colname+'_m15')
        
    zcol_ctx_selected_columns.append(zone_colname)
    return zcol_ctx_selected_columns
  

def get_zone_columns_list_as_ids(t:str):
    """
    Get the list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    Parameters:
    t (str): The timeframe to get the list of ZONE features for.
    
    Returns:
    list: The list of columns that are ZONE features for the given timeframe and its related timeframes.
    
    """
    
    zone_id_col_ctx_selected_columns = [ZONE_INT+'_M1',ZONE_INT+'_W1']
    
    if t=='H4' or t=='H8' or t=='H6' or t=='H1' or t=='m15' or t=='m5':
      zone_id_col_ctx_selected_columns.append(ZONE_INT+'_D1')
      
    if t=='H1' or t=='m15' or t=='m5':
        zone_id_col_ctx_selected_columns.append(ZONE_INT+'_H4')
        
    if t=='m15' or t=='m5':
        zone_id_col_ctx_selected_columns.append(ZONE_INT+'_H1')
    
    if t=='m5':
        zone_id_col_ctx_selected_columns.append(ZONE_INT+'_m15')
        
    zone_id_col_ctx_selected_columns.append(ZONE_INT)
    return zone_id_col_ctx_selected_columns
  
def column_zone_str_in_dataframe_to_id(df:pd.DataFrame,t:str,inplace=False,zone_colname=""):
    """
    Convert the ZONE columns from str to id in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The dataframe to convert the ZONE columns from str to id.
    t (str): The timeframe to convert the ZONE columns from str to id.
    inplace (bool): If True, the conversion is done in place. If False, a copy of the dataframe is returned with the conversion done.
    zone_colname (str): The name of the ZONE column to use. If not provided, the default ZCOL is used. (Planning to use ZONE_SIGNAL)
    
    Returns:
    pd.DataFrame: The dataframe with the ZONE columns converted from str to id.
    
    """
    if zone_colname=="":
        zone_colname=ZCOL
        
    if not inplace:
        df = df.copy()
    zcol_features_columns_list = get_zone_columns_list(t,zone_colname)
    for col_name in zcol_features_columns_list:
        df[col_name] = df[col_name].apply(lambda x: int(zonecolor_str_to_id(x)))
          #zonecolor_str_to_id)
    return df

def _zoneint_add_lagging_feature(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True,zone_colname=""):
    if zone_colname=="":
        zone_colname=ZCOL
        
    if not inplace:
        df = df.copy()
    columns_to_add_lags_to = get_zone_columns_list(t,zone_colname)
    columns_to_add_lags_to.append(zone_colname) #We want a lag for the current TF
    anhelper.add_lagging_columns(df, columns_to_add_lags_to, lag_period, total_lagging_periods, out_lag_midfix_str)
    for col in columns_to_add_lags_to:#@STCIssue Isn't that done already ???  Or it thinks they are Double !!!!
        for j in range(1, total_lagging_periods + 1):
            df[f'{col}{out_lag_midfix_str}{j}']=df[f'{col}{out_lag_midfix_str}{j}'].astype(int)
    return df
    

def wf_mk_zone_ready_dataset__240708(df: pd.DataFrame, t, lag_period=1, total_lagging_periods=5,out_lag_midfix_str='_lag_',inplace=True,zone_colname=""):
    if zone_colname=="":
        zone_colname=ZCOL
        
    if not inplace:
        df = df.copy()
    column_zone_str_in_dataframe_to_id(df,t,inplace=True,zone_colname=zone_colname)
    _zoneint_add_lagging_feature(df,t,lag_period=lag_period, total_lagging_periods=total_lagging_periods,out_lag_midfix_str=out_lag_midfix_str,inplace=True,zone_colname=zone_colname)
    return df