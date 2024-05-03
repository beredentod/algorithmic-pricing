'''
File: util_distance_duration_02.py

- create control variables for the stations regarding the distance in min to the next station
'''

import pandas as pd
from load_data_0 import df_char

df_dist = pd.read_csv('../data/distance_duration_10min.csv')

count1 = df_dist[df_dist['duration'] < 120].groupby('location_id_1').size()
count2 = df_dist[df_dist['duration'] < 300].groupby('location_id_1').size()
count3 = df_dist[df_dist['duration'] < 600].groupby('location_id_1').size()
minima = df_dist.groupby('location_id_1')['duration'].min()

count1.name = 'under_2min'
count2.name = 'under_5min'
count3.name = 'under_10min'
minima.name = 'minim_time_next'

result_df = pd.merge(count1.reset_index(), count2.reset_index(), on='location_id_1', how='outer')
result_df = pd.merge(result_df, count3.reset_index(), on='location_id_1', how='outer')
result_df = pd.merge(result_df, minima.reset_index(), on='location_id_1', how='outer')

result_df.columns = ['location_id', 'under_2min', 'under_5min', 'under_10min', 'minim_time_next']

result_df.fillna(0, inplace=True)

result_df['under_2min'] = result_df['under_2min'].astype(int)
result_df['under_5min'] = result_df['under_5min'].astype(int)

print(result_df)

df_char = pd.merge(df_char, result_df, on='location_id', how='inner')

print(df_char)

#df_char.to_csv('../data/stations_characteristics_MUC_long.csv', index=False)
#print('Saved!')