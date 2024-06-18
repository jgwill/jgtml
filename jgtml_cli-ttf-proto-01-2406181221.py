import argparse
import pandas as pd
from jgtpy import JGTCDSSvc as svc
from jgtutils import jgtpov as jpov
from jgtutils.jgtconstants import (MFI_VAL, ZCOL, AO)

columns_to_get_from_higher_tf = [MFI_VAL, ZCOL, AO]


def create_ttf_csv(instrument, timeframe, use_full=False, use_fresh=True, quotescount=333):
    povs = jpov.get_higher_tf_array(timeframe)
    ttf = pd.DataFrame()

    for pov in povs:
        cdf_datasets = svc.get_higher_cdf_datasets(instrument, timeframe, use_full=use_full, use_fresh=use_fresh, quotescount=quotescount, quiet=True)

        for k in cdf_datasets:
            v = cdf_datasets[k]
            for c in columns_to_get_from_higher_tf:
                new_col_name = c + "_" + k
                ttf[new_col_name] = None

                for ii, row in ttf.iterrows():
                    date = ii
                    data = v[v.index <= date]
                    if not data.empty:
                        data = data.iloc[-1]
                        ttf.at[ii, new_col_name] = data[c]

    output_filename = f"{instrument}_{timeframe}_ttf.csv"
    ttf.to_csv(output_filename, index=False)
    print(f"Output CSV file '{output_filename}' created successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ttf CSV file")
    parser.add_argument("-i", "--instrument", required=True, help="Instrument name")
    parser.add_argument("-t", "--timeframe", required=True, help="Timeframe (e.g., D1, H4)")
    parser.add_argument("-f", "--use_full", action="store_true", help="Use full dataset")
    parser.add_argument("-r", "--use_fresh", action="store_true", help="Use fresh data")
    parser.add_argument("-q", "--quotescount", type=int, default=333, help="Number of quotes to retrieve (default: 333)")

    args = parser.parse_args()
    create_ttf_csv(args.instrument, args.timeframe, args.use_full, args.use_fresh, args.quotescount)
