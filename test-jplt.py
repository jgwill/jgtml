# %% Imports

from jgtml import jplt
from jgtml.jplt import (
    _crop_dataframe,
    an_biv_plt2ds,
    an_bivariate_plot00,
    an_bivariate_plot00_four_features_v2,
)
from jgtml import jtc

import seaborn as sns 
import matplotlib.pyplot as plt
#%matplotlib inline



# %%


# %% Contexts

i = "GBP/USD"
i = "SPX500"

t = "H1"
t = "H4"
t = "D1"

dt_crop_last_DS2 = "2022-10-13"
dt_crop_last = "2018-08-14"
dt_crop_last = "2024-01-12 02:00:00"
dt_crop_last = None
dt_crop_last = "2023-07-20"
dt_crop_last = "2020-03-01"


ifn = i.replace("/", "-")

# df = pd.read_csv(idsfilepath)
df = jtc.readMXFile(i, t)
df2 = df.copy()
l = len(df)
print("len(df):", l)

verbose = 0

if verbose > 0:
    print(df.tail(1))


# %% Keeps NB Bars equals in the two datasets
n = -1
n = 120


if dt_crop_last is not None:
    df = _crop_dataframe(
        df, crop_last_dt=dt_crop_last, crop_start_dt=None, keep_amount=n
    )

df2 = _crop_dataframe(
    df2, crop_last_dt=dt_crop_last_DS2, crop_start_dt=None, keep_amount=n
)

# %% Select the columns only if target is not 0
df1t = df[(df["target"] != 0)].copy()
df2t = df2[(df2["target"] != 0)].copy()

# %% print len
print("len(df1t):", len(df1t))
#print(df1t.tail(1))
# %% Pairplot
# Painplot

# selected = df1t[["ao", "ac", "jaw", "teeth", "lips", "target"]]
columns_to_plot = ["ao", "ac", "jaw","target"]
columns_to_plot = ["ao", "ac", "jaw"]
selected = df[columns_to_plot]
selected2 = df2[columns_to_plot]

pp1 = jplt.pairplot(selected, title="Pairplot - " + dt_crop_last)
pp2 = jplt.pairplot(selected2, title="Pairplot - " + dt_crop_last_DS2)

# SupportsDataframe

# %% Pairgrid 
# pp1  Pairgrid

g = sns.PairGrid(selected)
g.map(plt.scatter)


# %% Pairgrid
# pp1  Pairgrid

jplt.pairgrid(selected, title="Pairgrid - " + dt_crop_last)

# %% Pairgrid
# pp2  Pairgrid

jplt.pairgrid(selected2, title="Pairgrid - " + dt_crop_last_DS2)

# %% Bivariate plot

an_bivariate_plot00(
    df,
    feature1="ao",
    target_variable="target",
    title="Bivariate Scatter Plot - " + dt_crop_last + " ",
)

an_bivariate_plot00(
    df2,
    feature1="ao",
    target_variable="target",
    title="Bivariate Scatter Plot - " + dt_crop_last_DS2 + " ",
)

# %%
an_bivariate_plot00(
    df1t,
    feature1="ao",
    target_variable="target",
    title="Bivariate Scatter Plot - " + dt_crop_last + " ",
)

an_bivariate_plot00(
    df2t,
    feature1="ao",
    target_variable="target",
    title="Bivariate Scatter Plot - " + dt_crop_last_DS2 + " ",
)

# %%
df2t

# %% Plot two points in time
an_biv_plt2ds(
    df,
    df2,
    feature1="ao",
    feature2="ao",
    target_variable="target",
    s0_title=str(n) + " rows - Scatter Plot NOW ",
    s1_title="Scatter Plot:" + dt_crop_last_DS2,
)

# %% Plot two points in time
an_biv_plt2ds(
    df,
    df2,
    feature1="ac",
    feature2="ac",
    target_variable="target",
    s0_title=str(n) + " rows - Scatter Plot NOW ",
    s1_title="Scatter Plot:" + dt_crop_last_DS2,
)
# %% 4 features

an_bivariate_plot00_four_features_v2(
    df,
    df2,
    dt_crop_last,
    dt_crop_last_DS2,
    feature1="ao",
    feature2="ac",
    target_variable="target",
    title="Bivariate Scatter Plot - " + dt_crop_last + " ",
)

# %% PLot distribution
jplt.an_distplot(df, feature="ao", title="Distribution of AO - " + dt_crop_last)

# %% PLot distribution
jplt.an_distplot(df2, feature="ao", title="Distribution of AO - " + dt_crop_last_DS2)


# %%

# %% PLot distribution
jplt.an_distplot(df, feature="target", title="Distribution of Target - " + dt_crop_last)

# %% PLot distribution
jplt.an_distplot(
    df2, feature="target", title="Distribution of Target - " + dt_crop_last_DS2
)


# %%
