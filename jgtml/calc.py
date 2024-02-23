#%% Imports
import pandas as pd
import os
from jgtpy import JGTPDSP as pds


#%% Functions

def crop_dataframe(df,crop_last_dt:str=None, crop_start_dt:str=None):
    if crop_last_dt is not None:
        df = df[df.index <= crop_last_dt]
    if crop_start_dt is not None:
        df = df[df.index >= crop_start_dt]
    return df

def calculate_target_variable_min_max(dfsrc, crop_last_dt=None, crop_start_dt=None, WINDOW_MIN=1, WINDOW_MAX=150, set_index=True, rounder=2,pipsize=-1):
    df = dfsrc.copy()
    
    df = crop_dataframe(df, crop_last_dt, crop_start_dt)
    
    
    #reset index before we iterate
    try:
        df.reset_index(drop=False, inplace=True)
    except:
        pass
    
    # Initialize the tmax and tmin columns with NaN values
    df['tmax'] = float('nan')
    df['tmin'] = float('nan')
    df['p'] = float('nan')
    df['l'] = float('nan')
    df['target'] = float('nan')

    # Calculate the maximum and minimum Close value in the window range for each row
    for i in range(WINDOW_MIN, len(df) - WINDOW_MAX):
        #FDBS
        if df.loc[i, 'fdbs'] == 1.0 :
            df.loc[i, 'tmax'] = df.loc[i:i+WINDOW_MAX, 'Close'].min()
            df.loc[i, 'tmin'] = df.loc[i:i+WINDOW_MAX, 'Close'].max()            
             
            if df.loc[i, 'High'] < df.loc[i, 'tmin']:
                df.loc[i, 'l'] = round(df.loc[i, 'High'] - df.loc[i, 'Low'], rounder)
                df.loc[i, 'target'] = round(-1 * (df.loc[i, 'High'] - df.loc[i, 'Low']), rounder)
            else:
                df.loc[i, 'p'] =  round(df.loc[i, 'Low'] - df.loc[i, 'tmax'], rounder)
                df.loc[i, 'target'] =  round(df.loc[i, 'Low'] - df.loc[i, 'tmax'], rounder)
        #FDBB    
        if df.loc[i, 'fdbb'] == 1.0:
            df.loc[i, 'tmax'] = df.loc[i:i+WINDOW_MAX, 'Close'].max()
            df.loc[i, 'tmin'] = df.loc[i:i+WINDOW_MAX, 'Close'].min()
            
            if df.loc[i, 'Low'] > df.loc[i, 'tmin']:
                df.loc[i, 'l'] = round(df.loc[i, 'High'] - df.loc[i, 'Low'], rounder)
                df.loc[i, 'target'] = round(-1*  (df.loc[i, 'High'] - df.loc[i, 'Low']), rounder)
            else:
                df.loc[i, 'p'] =round(df.loc[i, 'tmax'] - df.loc[i, 'High'] , rounder)
                df.loc[i, 'target'] =round(df.loc[i, 'tmax'] - df.loc[i, 'High'] , rounder)
            



    # Fill NaN with zero for columns tmax and tmin
    df['tmax']= df['tmax'].fillna(0)
    df['tmin']= df['tmin'].fillna(0)
    df['p']= df['p'].fillna(0)
    df['l']= df['l'].fillna(0)
    df['target']= df['target'].fillna(0)
    # After calculating the 'target' column
    if pipsize != -1:
        df['target'] = df['target'] / pipsize

    #@q Maybe set backnthe index !??
    if set_index:
        df.set_index('Date', inplace=True)
    return df


