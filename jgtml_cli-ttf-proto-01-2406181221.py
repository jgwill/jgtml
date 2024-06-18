import argparse
import pandas as pd
from jgtpy import JGTCDSSvc as svc
from jgtutils import jgtpov as jpov
from jgtutils.jgtconstants import (MFI_VAL, ZCOL, AO)

columns_to_get_from_higher_tf = [MFI_VAL, ZCOL, AO]

def make_htf_created_columns_array(workset,t):
    created_columns=[]
    for c in columns_to_get_from_higher_tf:
      for k in workset:
        if not c in created_columns: 
          created_columns.append(c)
        new_col_name = c+"_"+k
        if k != t:
          if not new_col_name in created_columns: 
            created_columns.append(new_col_name)
    return created_columns

def create_ttf_csv(i, t, use_full=False, use_fresh=True, quotescount=333):
    povs = jpov.get_higher_tf_array(t)
    ttf = pd.DataFrame()

    workset = svc.get_higher_cdf_datasets(i, t, use_full=use_full, use_fresh=use_fresh, quotescount=quotescount, quiet=True)
    ttf=workset[t]
    created_columns = make_htf_created_columns_array(workset, t)
    

    for k in workset:  
      if k!=t:
        v=workset[k]
        for c in columns_to_get_from_higher_tf:
        
          new_col_name = c+"_"+k
          ttf[new_col_name]=None

          for ii, row in ttf.iterrows():
            #get the date of the current row (the index)
            date = ii
            #print(k)
            data = v[v.index <= date]
            if not data.empty:
              data = data.iloc[-1]
              ttf.at[ii,new_col_name]=data[c]
    
    columns_we_want_to_keep_to_view=created_columns
    ttf_sel=ttf[columns_we_want_to_keep_to_view].copy()
    ifn=i.replace("/","-")
    output_filename = f"{ifn}_{t}_ttf.csv"
    output_filename_sel = f"{ifn}_{t}_ttf_sel.csv"
    ttf.to_csv(output_filename, index=True)
    ttf_sel.to_csv(output_filename_sel, index=True)
    print(f"Output CSV file '{output_filename}' created successfully.")
    print(f"Output CSV file '{output_filename_sel}' created successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ttf CSV file")
    parser.add_argument("-i", "--instrument", required=True, help="Instrument name")
    parser.add_argument("-t", "--timeframe", required=True, help="Timeframe (e.g., D1, H4)")
    parser.add_argument("-uf", "--full", action="store_true", help="Use full dataset")
    parser.add_argument("-new", "--fresh", action="store_true", help="Use fresh data")
    parser.add_argument("-c", "--quotescount", type=int, default=333, help="Number of quotes to retrieve (default: 333)")

    args = parser.parse_args()
    create_ttf_csv(args.instrument, args.timeframe, args.full, args.fresh, args.quotescount)
