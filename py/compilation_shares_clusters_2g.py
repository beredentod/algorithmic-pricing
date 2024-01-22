from datetime import datetime
import pandas as pd
import numpy as np

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char

#brand = 'aral'

cluster = 'group85' # cluster category

#df_char = df_char[df_char['brand_id'] == brand]

# check number of stations
#print(df_price_inc['id_data_updated'].nunique())

# check
#elements_not_in_b = [elem for elem in df_char[cluster].unique() if elem not in df_price_inc[cluster].unique()]
#print(df_char[df_char[cluster].isin(elements_not_in_b)])

#grouped = df_price_inc.groupby(cluster)

#for name, group in grouped:
#	print(name, group['id_data_updated'].nunique())

# the new data frame by taking all clusters for the time period of the dataset
df_shares = pd.DataFrame(df_price_inc[cluster].sort_values().unique(), columns=[cluster])

# big oil brands relevant
brands = ['aral', 'shell', 'esso', 'total', 'jet', 'agip', 'avia', 'bft', 'star', 'hem', 'omv']

# create new columns
df_shares['total_num_stations'] = np.nan
df_shares['total_num_price_inc'] = np.nan

for i in brands:
	df_shares['share_stations_'+i] = np.nan
	df_shares['share_price_inc_'+i] = np.nan

df_shares['share_stations_other'] = np.nan
df_shares['share_price_inc_other'] = np.nan


# for each cluster calculate the shares
for index, row in df_shares.iterrows():
    
    # rows are price increases that involve just the iterated cluster
    iter_cluster = df_price_inc[df_price_inc[cluster] == row[cluster]]

    total_inc = len(iter_cluster) # take the total number of increases with this cluster
    total_stat = iter_cluster['id_data_updated'].nunique() # take the number of unique stations

    df_shares.at[index, 'total_num_price_inc'] = total_inc
    df_shares.at[index, 'total_num_stations'] = total_stat

    # for each relevant brand: select a subset of increases with just this brand 
    for i in brands:
        brand_stations = iter_cluster[iter_cluster['brand_id'] == i]
        df_shares.at[index, 'share_stations_'+i] = brand_stations['id_data_updated'].nunique()/total_stat
        df_shares.at[index, 'share_price_inc_'+i] = len(brand_stations)/total_inc
       
    other_stations = iter_cluster[~iter_cluster['brand_id'].isin(brands)]
    df_shares.at[index, 'share_stations_other'] = other_stations['id_data_updated'].nunique()/total_stat
    df_shares.at[index, 'share_price_inc_other'] = len(other_stations)/total_inc


df_shares['total_num_stations'] = df_shares['total_num_stations'].astype(int)
df_shares['total_num_price_inc'] = df_shares['total_num_price_inc'].astype(int)

print(df_shares)

df_shares.to_csv('../data/share_price_inc_MUC_'+cluster+'.csv', index=False)