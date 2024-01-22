from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char


'''
df_price_inc = df_price_inc.drop('brand_id', axis=1)

df_char_fil = df_char[['id_data_updated', 'brand_id']]

result_df = pd.merge(df_price_inc, df_char_fil, on='id_data_updated', how='left')

result_df = result_df[['id_data_updated', 'date', 'time', 'dow', 'brand_id', 'price', 'change', 'cycle',
       'bool_cycle_begin', 'group80', 'group85', 'group90']]
'''



'''
print(df_price_inc)

merged_df = pd.merge(df_price_inc, df_char[['id_data_updated', 'brand_id']], on='id_data_updated', how='left')

# Update 'brand_id' column in df_price_inc with values from merged_df
df_price_inc['brand_id'] = merged_df['brand_id']

df_price_inc = df_price_inc[['id_data_updated', 'date', 'time', 'dow', 'brand_id', 'price', 'change', 'cycle',
       'bool_cycle_begin', 'group80', 'group85', 'group90']] 

print(df_price_inc)

df_price_inc.to_csv('../data/price-increases_all-DE_12-2022_price-leaders.csv')
print('Saved!')'''


df_price_inc['cycle_leader80'] = 0
df_price_inc['mult_leader80'] = 0

df_price_inc['cycle_leader85'] = 0
df_price_inc['mult_leader85'] = 0

df_price_inc['cycle_leader90'] = 0
df_price_inc['mult_leader90'] = 0

cluster = 'group85'

#print(df_price_inc)

#grouped = df_price_inc.groupby(['date', 'group80', 'cycle'])


grouped = df_price_inc.sort_values(['time']).groupby(['date', 'group80', 'cycle'])

for _, group in grouped:
	
	times = group.groupby(['time'])
	first = times.get_group((list(times.groups)[0]))

	df_price_inc.loc[first.index, 'cycle_leader80'] = 1

	if len(first) > 1:
		df_price_inc.loc[first.index, 'mult_leader80'] = 1


df_price_inc = df_price_inc.reset_index(drop=True)


print(df_price_inc)


grouped = df_price_inc.sort_values(['time']).groupby(['date', 'group85', 'cycle'])

for _, group in grouped:
	
	times = group.groupby(['time'])
	first = times.get_group((list(times.groups)[0]))

	df_price_inc.loc[first.index, 'cycle_leader85'] = 1

	if len(first) > 1:
		df_price_inc.loc[first.index, 'mult_leader85'] = 1


df_price_inc = df_price_inc.reset_index(drop=True)


print(df_price_inc)


grouped = df_price_inc.sort_values(['time']).groupby(['date', 'group90', 'cycle'])

for _, group in grouped:
	
	times = group.groupby(['time'])
	first = times.get_group((list(times.groups)[0]))

	df_price_inc.loc[first.index, 'cycle_leader90'] = 1

	if len(first) > 1:
		df_price_inc.loc[first.index, 'mult_leader90'] = 1

df_price_inc = df_price_inc.reset_index(drop=True)


df_price_inc = df_price_inc[['id_data_updated', 'date', 'time', 'dow', 'brand_id', 'price', 'change', 'cycle',
       'bool_cycle_begin', 'group80', 'group85', 'group90', 'cycle_leader80', 'mult_leader80', 'cycle_leader85', 'mult_leader85', 'cycle_leader90', 'mult_leader90']] 

print(df_price_inc)

#df_prices_inc = df_price_inc[(df_price_inc['brand_id'] == 'shell') & (df_price_inc['cycle_leader'] == 1)]

#print((df_price_inc[df_price_inc['cycle_leader'] == 1].groupby('brand_id').size()).sort_values(ascending=False))

#filtered = df_price_inc[df_price_inc['mult_leader'] == 0]

#print((filtered[filtered['cycle_leader'] == 1].groupby('brand_id').size()).sort_values(ascending=False))



df_price_inc.to_csv('../data/price-increases_all-DE_12-2022_price-leaders.csv', index=False)
print('Saved!')





