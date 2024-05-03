from datetime import datetime
import pandas as pd
import numpy as np

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char


cluster = 'group85' # cluster category

df_price_inc = df_price_inc.drop(columns=['group80', 'cycle_leader80', 'mult_leader80', 'group90', 'cycle_leader90', 'mult_leader90'])

# big oil brands relevant
brands = ['aral', 'shell', 'esso', 'total', 'jet', 'agip', 'avia', 'bft', 'star', 'hem', 'omv']


df_exp_obs = pd.read_csv('../data/first_movers_exp-obs_all-DE_10-2022_group85.csv')

df_exp_obs['margin_first-movership'] = df_exp_obs['observed'] / df_exp_obs['expected']

df_otherbrands = df_exp_obs[~df_exp_obs['brand_id'].isin(brands)].reset_index()

df_brands = df_exp_obs.groupby('brand_id').agg({'margin_first-movership': 'mean'}).reset_index()

df_brands = df_brands[df_brands['brand_id'].isin(brands)].reset_index()


# Create a new row for 'other' brands
other_row = pd.DataFrame({
    'brand_id': ['other'],
    'margin_first-movership': [df_otherbrands['margin_first-movership'].mean()],
})

# Concatenate the 'other' row to df_brands
df_brands = pd.concat([df_brands, other_row], ignore_index=True)


df_brands = df_brands.drop(columns='index')

print(df_brands)
