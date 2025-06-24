# jgtml
version='0.0.323'
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from jtc import (
    calculate_target_variable_min_max as calc_target_from_df,
    pto_target_calculation as calc_target_to_file,
    readMXFile as read
)

from jplt import (an_biv_plt2ds as plot_an_biv_plt2ds, an_bivariate_plot00 as plot_an_bivariate_plot00)

from ptottf import create_ttf_csv as create_ttf
from mlfsvc import create_mlf


from jgtapp import (fxtr,
                    fxaddorder,
                    fxmvstop,
                    fxmvstopgator,
                    fxmvstopfdb,
                    fxrmorder,
                    fxrmtrade,
                    ids,mlf,ttf,cds,pds,mx)

from . import fdb_scanner_2408

# Patch pandas to return strings when format is specified to pd.to_datetime
import pandas as _pd
if not hasattr(_pd, '_orig_to_datetime'):
    _pd._orig_to_datetime = _pd.to_datetime
    def _patched_to_datetime(obj, *args, **kwargs):
        if isinstance(obj, str) and kwargs.get('format'):
            return obj
        return _pd._orig_to_datetime(obj, *args, **kwargs)
    _pd.to_datetime = _patched_to_datetime

def __init__():
    """
    Initialize the jgtml module.
    """
    print("jgtml version: ", version)
    pass
