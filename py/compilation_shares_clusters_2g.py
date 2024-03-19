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
df_shares['total_num_first_movers'] = np.nan

for i in brands:
    df_shares['share_stations_'+i] = np.nan
    df_shares['share_first_movers_'+i] = np.nan
    df_shares['share_diff_'+i] = np.nan

df_shares['share_stations_other'] = np.nan
df_shares['share_first_movers_other'] = np.nan
df_shares['share_diff_other'] = np.nan


clusters = [162, 194, 384, 403, 1433, 1832, 2047, 2183, 2682, 3018]


# for each cluster calculate the shares
for index, row in df_shares.iterrows():
    
    # rows are price increases that involve just the iterated cluster
    iter_cluster = df_price_inc[df_price_inc[cluster] == row[cluster]]

    iter_cluster_leaders = iter_cluster[iter_cluster['cycle_leader85'] == 1]

    total_fm = len(iter_cluster_leaders) # take the total number increases in cluster which are first movers
    total_stat = iter_cluster['id_data_updated'].nunique() # take the number of unique stations

    df_shares.at[index, 'total_num_first_movers'] = total_fm
    df_shares.at[index, 'total_num_stations'] = total_stat

    # for each relevant brand: select a subset of increases with just this brand 
    for i in brands:
        brand_inc = iter_cluster[iter_cluster['brand_id'] == i]
        brand_stat = brand_inc['id_data_updated'].nunique()
        brand_fm = brand_inc[brand_inc['cycle_leader85'] == 1]

        df_shares.at[index, 'share_stations_'+i] = brand_stat/total_stat
        df_shares.at[index, 'share_first_movers_'+i] = len(brand_fm)/total_fm
       

    other_station_inc = iter_cluster[~iter_cluster['brand_id'].isin(brands)]
    other_stat = other_station_inc['id_data_updated'].nunique()
    other_fm = other_station_inc[other_station_inc['cycle_leader85'] == 1]

    df_shares.at[index, 'share_stations_other'] = other_stat/total_stat
    df_shares.at[index, 'share_first_movers_other'] = len(other_fm)/total_fm


df_shares['total_num_stations'] = df_shares['total_num_stations'].astype(int)
df_shares['total_num_first_movers'] = df_shares['total_num_first_movers'].astype(int)

for i in brands:
    df_shares['share_diff_'+i] = df_shares['share_first_movers_'+i] - df_shares['share_stations_'+i]

df_shares['share_diff_other'] = df_shares['share_first_movers_other'] - df_shares['share_stations_other']

pd.set_option('display.max_rows', None)
print(df_shares)

#df_shares.to_csv('../data/share_first_movers_all-DE_'+cluster+'.csv', index=False)