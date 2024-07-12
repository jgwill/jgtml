import pandas as pd

pd.options.mode.copy_on_write = True
#PerformanceWarning
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


def add_lagging_columns(dfsrc: pd.DataFrame, columns_to_add_lags_to, lag_period=1, total_lagging_periods=5, out_lag_midfix_str='_lag_',dropna=True):
  for col in columns_to_add_lags_to:
    if col not in dfsrc.columns:
      print("WARN::Column not in dataframe:", col, " Skipping")
      pass
    else:
      for j in range(1, total_lagging_periods + 1):
      # Using .loc to ensure the operation is done without warnings
        dfsrc.loc[:, f'{col}{out_lag_midfix_str}{j}'] = dfsrc[col].shift(j * lag_period)
  # Drop rows where there are no lag values
  if dropna:
    dfsrc.dropna(inplace=True)
    
  for col in columns_to_add_lags_to: #@STCIssue Isn't that done already ???  Or it thinks they are Double !!!!
    for j in range(1, total_lagging_periods + 1):
      dfsrc[f'{col}{out_lag_midfix_str}{j}']=dfsrc[f'{col}{out_lag_midfix_str}{j}'].astype(int)
  return dfsrc
