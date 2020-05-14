# ---
# jupyter:
#   jupytext:
#     formats: notebooks//ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: fastai
#     language: python
#     name: fastai
# ---

# %%
import pandas as pd

# %%
FILENAME = '../strategies.csv'

# %%
df = pd.read_csv(FILENAME)

# %%
df.head()


# %%
def foo(x):
    if x is troop_name:
        return 1
    else:
        return 0

new_cols = [df.columns[0]]
df_bool = df.copy()
for i, col in enumerate(df.columns[1:]):
    troop_name = [x for x in df.loc[:, col].unique() if type(x) is str][0]
    df_bool.loc[:, col] = df.loc[:, col].map(lambda x: x is troop_name)
    new_cols.append(troop_name)

df_bool.columns = pd.Index(new_cols)

# %%
df_bool.head()

# %%
