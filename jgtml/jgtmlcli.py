#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# import .

from jgtutils import (
    jgtcommon as jgtcommon
)
import argparse




import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Process command parameters.")
    # jgtfxcommon.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    
    jgtcommon.add_tlid_range_argument(parser)
    
    jgtcommon.add_verbose_argument(parser)
    
    jgtcommon.add_use_full_argument(parser)

    # jgtcommon.add_cds_argument(parser)
    args = parser.parse_args()
    return args


def main():
    
    args = parse_args()
    instrument = args.instrument
    timeframe = args.timeframe
    
    full = False
    if args.full:
        full = True

    date_from = None
    date_to = None
    tlid_range = None
    if args.tlidrange:
        # @STCGoal Get range prices from cache or request new
        tlid_range = args.tlidrange
        print("FUTURE Support for tlid range")
        
        print("-----------Stay tune -------- Quitting for now")
        return


        

    
    verbose_level = args.verbose
    quiet = False
    if verbose_level == 0:
        quiet = True
    

    if verbose_level > 1:
        if date_from:
            print("Date from : " + str(date_from))
        if date_to:
            print("Date to : " + str(date_to))

    try:

        print_quiet(quiet, "Getting for : " + instrument + "_" + timeframe)
        instruments = instrument.split(",")
        timeframes = timeframe.split(",")

        for instrument in instruments:
            for timeframe in timeframes:
                print("-------TO IMPLEMENT Creating Target MX for: " + instrument + "_" + timeframe)

    except Exception as e:
        jgtcommon.print_exception(e)

    # try:
    #    jgtpy.off()
    # except Exception as e:
    #    jgtfxcommon.print_exception(e)


# if __name__ == "__main__":
#     main()

# print("")
# #input("Done! Press enter key to exit\n")


def createMX_for_main(
    instrument,
    timeframe,
    quiet,
    verbose_level=0,
    tlid_range=None,
    use_full=False,
):
    print("----TODO:  createMX_for_main")

def print_quiet(quiet, content):
    if not quiet:
        print(content)


if __name__ == "__main__":
    main()
