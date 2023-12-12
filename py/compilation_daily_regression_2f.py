import datetime
import pandas as pd
import numpy as np

import functions_1 as fcs
from functions_1 import df_daily_station_linreg
from functions_1 import df_char

'''
df1 = pd.read_csv('../data/stations_prices_all_DE_10-2022_station-reg.csv')
df2 = pd.read_csv('../data/stations_prices_all_DE_11-2022_station-reg.csv')
df3 = pd.read_csv('../data/stations_prices_all_DE_12-2022_station-reg.csv')

concat = pd.concat([df1, df2, df3], axis=0, join='outer', ignore_index=True)

cluster_char = pd.read_csv('../data/group85_all_characteristics.csv')

concat = pd.merge(concat, df_char[['id_data_updated', 'verf_inc_pp', 'density', 'under_5min', 'minim_time_next']], on="id_data_updated", how='inner')

concat = pd.merge(concat, cluster_char[['group85', 'n' ,'share_indep']], on='group85', how='inner')

concat = concat.rename(columns={'n': 'cluster_size'})
'''


concat = pd.read_csv('../data/regression_stations_all_DE_Oct-Dec-2022.csv')

'''
concat = pd.merge(concat, df_char[['id_data_updated', 'brand_id', 'location_id']], on='id_data_updated', how='inner')

concat = concat[['id_data_updated', 'date', 'group85', 'brand_id', 'location_id', 'price_mean', 'price_17h',
       'price_18h', 'verf_inc_pp', 'density', 'under_5min', 'minim_time_next',
       'cluster_size', 'share_indep']]
'''



dummies = pd.get_dummies(concat['date'], prefix='date')

print(dummies)

concat = pd.concat([concat, dummies], axis=1)

print(concat)

filename = '../data/regression_stations_all_DE_Oct-Dec-2022_with-dummies.csv'
concat.to_csv(filename, index=False)
print('Saved: ' + filename)
