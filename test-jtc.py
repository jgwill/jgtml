#%% Imports
import pandas as pd
from jgtml import jtc

#%% read

df=pd.read_csv('Data.cds.csv',index_col=0,parse_dates=True)


# %%
df
# %%
# Calculate target
mxdf = jtc.calculate_target_variable_min_max(df)

mxdf
# %%
# pto_target_calculation save_outputs
i="GBP/USD";t="D1"
sel_2_keeping_columns=["Open", "High", "Low", "Close", "fdbs","zlcb", "fdbb","zlcs", "target"]

mxdf,sel1,sel2 = jtc.pto_target_calculation(i,
                                            t,
                                            pto_vec_fdb_ao_vector_window_flag=True,
                                            save_outputs=False,
                                            write_reporting=False,
                                            sel_2_keeping_columns=sel_2_keeping_columns,
                                            )

# %%
mxdf
# %%
sel1
# %%
sel2
# %%

mxdfb,sel1b,sel2b = jtc.pto_target_calculation(i,
                                               t,
                                               pto_vec_fdb_ao_vector_window_flag=True,
                                               save_outputs=True,write_reporting=False,sel_2_keeping_columns=sel_2_keeping_columns,
                                               WINDOW_MIN=1,
                                               WINDOW_MAX=75,
                                            )

# %%
mxdfb
# %%
sel1b
# %%
sel2b
# %%
