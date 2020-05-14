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
FILE_STRATEGY = '../strategies.csv'
FILE_UPGRADE = '../upgrades.csv'

# %%
df = pd.read_csv(FILE_STRATEGY)

# %%
df.head()


# %%
def foo(x):
    if x is troop_name:
        return 1
    else:
        return 0

new_cols = [df.columns[0]]
strategies = df.copy()
for i, col in enumerate(df.columns[1:]):
    troop_name = [x for x in df.loc[:, col].unique() if type(x) is str][0]
    strategies.loc[:, col] = df.loc[:, col].map(lambda x: x is troop_name)
    new_cols.append(troop_name)

for i, col in enumerate(new_cols):
    if col in ['Earthquake', 'Haste', 'Poison']:
        new_cols[i] = col + " Spell"
    if col == 'Balloons':
        new_cols[i] = col[:-1]
        
strategies.columns = pd.Index(new_cols)

# %%
strategies.head()

# %% [markdown]
# ## Include upgrade levels and lengths

# %%
df = pd.read_csv(FILE_UPGRADE)

# %%
df.head()


# %%
def add_time(x):
    if type(x) is str:
        if '/' in x:
            return sum(map(float, x.split('/')))
        
    return x

def max_level(x):
    if type(x) is str:
        if '/' in x:
            return max(map(float, x.split('/')))
        
    return x

upgrade = df.copy()

upgrade.loc[:, 'Troop'] = df['Troop'].map(lambda x: x.strip())
upgrade.loc[:, 'Category'] = df['Category'].map(lambda x: x.strip())

for col in upgrade.columns[2:]:
    upgrade.loc[upgrade['Category'] == 'Time', col] = upgrade[upgrade['Category'] == 'Time'][col].map(add_time)
    upgrade.loc[upgrade['Category'] == 'Level', col] = upgrade[upgrade['Category'] == 'Level'][col].map(max_level)
    upgrade.loc[upgrade[col].isna(), col] = ' '

# %%
upgrade.head(60)

# %% [markdown]
# ## Lets enumerate all combinations of choices and add the total time

# %%
for th 8:
    for th 9:
        for th 10:
            for th 11:
                for th 12:
                    for th 13:
