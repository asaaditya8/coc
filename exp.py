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
FILE_MAX_LVL = '../max_level.csv'
FILE_UPGRADE = '../upgrades_level_wise.csv'

# %%
df = pd.read_csv(FILE_STRATEGY)


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

# %% [markdown]
# ## Lets enumerate all combinations of choices and add the total time

# %%
strategies.loc[strategies['TH'] == 9]

# %% [markdown]
# + Pick 1 strategy at th 8 upgrade only those troops rest remain at current levels
# + Pick 1 strategy at th 9 upgrade only those troops rest remain at current levels

# %% [markdown]
# This makes the previous work on upgrades a waste.
# Lets re-do it.

# %% [markdown]
# ## Upgrades with Level Tracking

# %% [markdown]
# ### Max Levels

# %%
df = pd.read_csv(FILE_MAX_LVL)

# %%
df.head()

# %%
for col1, col2 in zip(df.columns[1:-1], df.columns[2:]):
    for i in df.index:
        try:
            int(df.loc[i, col2])
        except:
            df.loc[i, col2] = df.loc[i, col1]
            
df.loc[:, 'Troop'] = df['Troop'].map(lambda x: x.strip())
max_levels = df.copy()

# %%
max_levels.head(70)

# %% [markdown]
# ### Upgrades

# %%
import numpy as np

# %%
upgrades = pd.read_csv(FILE_UPGRADE)

# %%
upgrades[upgrades == ' '] = np.NaN
# upgrades = upgrades.fillna(0)

upgrades.loc[:, 'Troop'] = upgrades['Troop'].map(lambda x: x.strip())
for col in range(2,11):
    upgrades.loc[:, str(col)] = upgrades[str(col)].map(float)

# %%
upgrades.head()


# %% [markdown]
# ### Current State

# %%
def correct_nan(x):
    try:
        return int(x)
    except:
        return 1

start_state = {k: correct_nan(v) for k, v in zip(max_levels['Troop'].values, max_levels['TH 6'].values) }

# %%
start_state

# %%
max_levels['Troop'].values

# %%
# make a choice
# get the update for the state
    # make a choice
    # get the update for the state
        # make a choice
        # get the update for the state
        # aggregate all updates

# %%
choice_log = {}
full_plan_times = []
counter = 0

def make_choice(choice_idx, th_lvl):
    mask = strategies.iloc[choice_idx, 1:].to_dict()
    lvl_updates = {troop: 0 for troop in start_state}

    total_time_for_th = 0
    
    current_state = {troop: start_state[troop] for troop in start_state}
    
    for j in range(8, th_lvl):
        for troop in current_state:
            current_state[troop] += choice_log[j]['lvl_incs'][troop]

    for troop in mask:
        if mask[troop]:
            max_lvl = max_levels[max_levels['Troop'] == troop]['TH ' + str(th_lvl)]
            try:
                max_lvl = int(max_lvl)
            except:
                max_lvl = 1

            # apply all updates till now

            level_inc = max_lvl - current_state[troop]
            time_inc = upgrades[ upgrades['Troop'] == troop ].iloc[0, current_state[troop]:max_lvl].sum()

            lvl_updates[troop] = level_inc
            total_time_for_th += time_inc

    choice_log[th_lvl] = {'lvl_incs': lvl_updates, 'time': total_time_for_th, 'choice': choice_idx}

    
plans = strategies.loc[strategies['TH'] == 8]
for choice_idx in plans.index:
    make_choice(choice_idx, 8)
    
    plans = strategies.loc[strategies['TH'] == 9]
    for choice_idx in plans.index:
        make_choice(choice_idx, 9)
        
        plans = strategies.loc[strategies['TH'] == 10]
        for choice_idx in plans.index:
            make_choice(choice_idx, 10)
            
            plans = strategies.loc[strategies['TH'] == 11]
            for choice_idx in plans.index:
                make_choice(choice_idx, 11)
                
                plans = strategies.loc[strategies['TH'] == 12]
                for choice_idx in plans.index:
                    make_choice(choice_idx, 12)
                    
#                     plans = strategies.loc[strategies['TH'] == 13]
#                     for choice_idx in plans.index:
#                         make_choice(choice_idx, 13)
                        
                    total_time = 0
                    result = {}
                    for th_lvl in range(8, 13):
                        total_time += choice_log[th_lvl]['time']
                        result['TH ' + str(th_lvl) + ' choice'] = choice_log[th_lvl]['choice']
                        result['TH ' + str(th_lvl) + ' time'] = choice_log[th_lvl]['time']

                    result['time'] = total_time
                    full_plan_times.append(result)

                    counter += 1
                    print(counter, end=' ')
                            


# %%
result = pd.DataFrame(full_plan_times)

# %%
cols = [x for x in result.columns if 'choice' in x]
for i in list(sorted(map(int, result.sort_values('time').loc[4, cols].values))) + [12]:
    record = strategies.iloc[i]
    th = record['TH']
    mask = record[strategies.columns[1:]]
    troops = mask[mask == True]
    row = [str(i), str(th)] + list(troops.index)
    for item in row[:2]:
        print( '%3s' % item, end=' ' )
    for item in row[2:]:
        print( '%13s' % item, end=' ' )
    print()

# %%
result.sort_values('time')

# %%
