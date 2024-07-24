"""
Common functions for various cli of the jgtml project

- instrument/timeframe arguments
- force_refresh
- columns_list_from_higher_tf
- bars_amount_V2_arguments
- use_fresh_argument
- dropna_volume_argument
- drop_bid_ask
- columns_to_keep
- columns_to_drop
- lag_period
- total_lagging_periods
- patternname

"""


import argparse
from jgtutils import jgtcommon


def __deprecate_force_read(args:argparse.Namespace):
  if args.force_read and args.force_read is True:
    print("force_read is deprecated.  Use --fresh instead")
  

def add_patterns_arguments(parser:argparse.ArgumentParser)->argparse.ArgumentParser:
  from jgtutils.jgtcommon import _get_group_by_title
  pn_group=_get_group_by_title(parser,"Patterns")
  pn_group.add_argument("-clh", "--columns_list_from_higher_tf", nargs='+', help="List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao", default=None)
  pn_group.add_argument("-pn", "--patternname", help="Pattern Name", default="ttf")
  
  return parser

