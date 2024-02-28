#%% Imports
import pandas as pd
import os
#import jgtml as jml
from jgtml import  jtc

from jgtml import jplt

import tlid
tlid_tag = tlid.get_minutes()


crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

instruments = I_raw.split(',')
timeframes = T_raw.split(',')



print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        jtc.pto_target_calculation(i,t)



