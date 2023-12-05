from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
from functions_1 import df_price_inc

df_price_inc['cycle_leader90'] = 0
df_price_inc['mult_leader90'] = 0

cluster = 'group90'

#print(df_price_inc)

#grouped = df_price_inc.groupby(['date', 'group80', 'cycle'])


grouped = df_price_inc.sort_values(['time']).groupby(['date', cluster, 'cycle'])

for _, group in grouped:
	
	times = group.groupby(['time'])
	first = times.get_group((list(times.groups)[0]))

	df_price_inc.loc[first.index, 'cycle_leader90'] = 1

	if len(first) > 1:
		df_price_inc.loc[first.index, 'mult_leader90'] = 1


df_price_inc = df_price_inc.reset_index(drop=True)


#print(df_price_inc)

#df_prices_inc = df_price_inc[(df_price_inc['brand_id'] == 'shell') & (df_price_inc['cycle_leader'] == 1)]

#print((df_price_inc[df_price_inc['cycle_leader'] == 1].groupby('brand_id').size()).sort_values(ascending=False))

#filtered = df_price_inc[df_price_inc['mult_leader'] == 0]

#print((filtered[filtered['cycle_leader'] == 1].groupby('brand_id').size()).sort_values(ascending=False))


#df_price_inc.to_csv('price-increases_MUC_Oct22_price-leaders.csv', index=False)
#print('Saved!')



