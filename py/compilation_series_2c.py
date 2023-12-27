from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
from functions_1 import df_linreg_prices
from functions_1 import df_char

import numpy as np


single_date = datetime(2022, 10, 5)
param = 'id_data_updated'
arg = 'f96b0d2b-c33b-4d8e-a08b-6a9e2f3c657a'




df_linreg_prices['timestamp'] = pd.to_datetime(df_linreg_prices['timestamp'])
df_linreg_prices['date'] = pd.to_datetime(df_linreg_prices['timestamp'].dt.date)


print(df_linreg_prices)

df_linreg_prices['change'] = np.nan
df_linreg_prices['bool_cycle_begin'] = np.nan
df_linreg_prices['cycle'] = np.nan


#df_linreg_prices = df_linreg_prices.loc[(df_linreg_prices['id_data_updated'] == arg) & (df_linreg_prices['date'] == single_date)]


#print(df_filter)


#selected_df = pd.DataFrame(columns=df_filter.columns)
#selected_rows = []


'''
stack_empty = True
first_done = False
cycle = 0
first_cycle = 0

first = df_filter.iloc[0]

first_time = first['timestamp'].time()

if  first_time < pd.to_datetime('09:00').time():
	first_cycle = 1
elif first_time >= pd.to_datetime('09:00').time() and first_time < pd.to_datetime('12:00').time(): 
	first_cycle = 2
elif first_time >= pd.to_datetime('12:00').time() and first_time < pd.to_datetime('15:00').time(): 
	first_cycle = 3
elif first_time >= pd.to_datetime('15:00').time() and first_time < pd.to_datetime('17:00').time(): 
	first_cycle = 4
elif first_time >= pd.to_datetime('17:00').time() and first_time < pd.to_datetime('19:00').time(): 
	first_cycle = 5
elif first_time >= pd.to_datetime('19:00').time() and first_time < pd.to_datetime('22:00').time(): 
	first_cycle = 6
elif first_time >= pd.to_datetime('22:00').time(): 
	first_cycle = 7


for i in range(1, len(df_filter)):
	prev = df_filter.iloc[i-1]
	curr = df_filter.iloc[i]
	first = df_filter.iloc[0]

	curr_time = curr['timestamp'].time()

	if  curr_time < pd.to_datetime('09:00').time():
		cycle = 1
	elif curr_time >= pd.to_datetime('09:00').time() and curr_time < pd.to_datetime('12:00').time(): 
		cycle = 2
	elif curr_time >= pd.to_datetime('12:00').time() and curr_time < pd.to_datetime('15:00').time(): 
		cycle = 3
	elif curr_time >= pd.to_datetime('15:00').time() and curr_time < pd.to_datetime('17:00').time(): 
		cycle = 4
	elif curr_time >= pd.to_datetime('17:00').time() and curr_time < pd.to_datetime('19:00').time(): 
		cycle = 5
	elif curr_time >= pd.to_datetime('19:00').time() and curr_time < pd.to_datetime('22:00').time(): 
		cycle = 6
	elif curr_time >= pd.to_datetime('22:00').time(): 
		cycle = 7


	if curr['price'] > prev['price']:

		if stack_empty == True:
			stack_empty = False
			curr.loc['change'] = curr['price'] - prev['price']
			curr.loc['bool_cycle_begin'] = 1
			curr.loc['cycle'] = cycle
			selected_rows.append(curr)
			first_done = True
			print('Increase + rec: ' + str(curr['price']))

		else:
			curr.loc['change'] = curr['price'] - prev['price']
			curr.loc['bool_cycle_begin'] = 0
			curr.loc['cycle'] = cycle
			selected_rows.append(curr)
			print('Increase: ' + str(curr['price']))


	elif curr['price'] < prev['price']:
		stack_empty = True
		print('Decrease: ' + str(curr['price']))

		if first_done == False:
			first.loc['change'] = 0
			first.loc['bool_cycle_begin'] = 1
			first.loc['cycle'] = first_cycle
			selected_rows.append(first)
			first_done = True
			print('Rec: ' + str(curr['price']))

	else:
		print('Stable: ' + str(curr['price']))

selected_df = pd.concat(selected_rows, axis=1).T
selected_df.reset_index(drop=True, inplace=True)

print(selected_df)
'''

'''
selected_rows = []

grouped_by_station = df_linreg_prices.groupby('id_data_updated')

for station_idx, group in grouped_by_station:
	grouped_by_date =  group.groupby('date')

	for date, group2 in grouped_by_date:

		stack_empty = True
		first_done = False
		cycle = 0
		first_cycle = 0

		first = group2.iloc[0]
		first_time = first['timestamp'].time()

		if  first_time < pd.to_datetime('09:00').time():
			first_cycle = 1
		elif first_time >= pd.to_datetime('09:00').time() and first_time < pd.to_datetime('12:00').time(): 
			first_cycle = 2
		elif first_time >= pd.to_datetime('12:00').time() and first_time < pd.to_datetime('15:00').time(): 
			first_cycle = 3
		elif first_time >= pd.to_datetime('15:00').time() and first_time < pd.to_datetime('17:00').time(): 
			first_cycle = 4
		elif first_time >= pd.to_datetime('17:00').time() and first_time < pd.to_datetime('19:00').time(): 
			first_cycle = 5
		elif first_time >= pd.to_datetime('19:00').time() and first_time < pd.to_datetime('22:00').time(): 
			first_cycle = 6
		elif first_time >= pd.to_datetime('22:00').time(): 
			first_cycle = 7


		for i in range(1, len(group2)):
			prev = group2.iloc[i-1]
			curr = group2.iloc[i]

			curr_time = curr['timestamp'].time()

			if  curr_time < pd.to_datetime('09:00').time():
				cycle = 1
			elif curr_time >= pd.to_datetime('09:00').time() and curr_time < pd.to_datetime('12:00').time(): 
				cycle = 2
			elif curr_time >= pd.to_datetime('12:00').time() and curr_time < pd.to_datetime('15:00').time(): 
				cycle = 3
			elif curr_time >= pd.to_datetime('15:00').time() and curr_time < pd.to_datetime('17:00').time(): 
				cycle = 4
			elif curr_time >= pd.to_datetime('17:00').time() and curr_time < pd.to_datetime('19:00').time(): 
				cycle = 5
			elif curr_time >= pd.to_datetime('19:00').time() and curr_time < pd.to_datetime('22:00').time(): 
				cycle = 6
			elif curr_time >= pd.to_datetime('22:00').time():
				cycle = 7

			if curr['price'] > prev['price']:

				if stack_empty == True:
					stack_empty = False
					df_linreg_prices.loc[curr.name, 'change'] = curr['price'] - prev['price']
					df_linreg_prices.loc[curr.name, 'bool_cycle_begin'] = 1
					df_linreg_prices.loc[curr.name, 'cycle'] = cycle
					selected_rows.append(curr)
					first_done = True

				else:
					#print('Increase: ' + str(curr['price']))
					df_linreg_prices.loc[curr.name, 'change'] = curr['price'] - prev['price']
					df_linreg_prices.loc[curr.name, 'bool_cycle_begin'] = 0
					df_linreg_prices.loc[curr.name, 'cycle'] = cycle
					selected_rows.append(curr)


			elif curr['price'] < prev['price']:
				stack_empty = True
				if first_done == False:
					df_linreg_prices.loc[first.name, 'change'] = 0
					df_linreg_prices.loc[first.name, 'bool_cycle_begin'] = 1
					df_linreg_prices.loc[first.name, 'cycle'] = first_cycle
					selected_rows.append(first)
					first_done = True
				#print('Decrease: ' + str(curr['price']))

			#else:
				#print('Stable: ' + str(curr['price']))

		

selected_df = pd.concat(selected_rows, axis=1).T
selected_df.reset_index(drop=True, inplace=True)
		
			
selected_df = selected_df.drop('date', axis=1)
selected_df['dow'] = selected_df['timestamp'].dt.day_name()
selected_df['brand_id'] = selected_df['id_data_updated'].map(df_char.set_index('id_data_updated')['brand_id'])

selected_df['date'] = selected_df['timestamp'].dt.date
selected_df['time'] = selected_df['timestamp'].dt.time

selected_df = selected_df.drop('timestamp', axis=1)

selected_df = selected_df[['id_data_updated', 'date', 'time', 'dow', 'brand_id', 'price', 'change', 'cycle', 'bool_cycle_begin', 'group80', 'group85', 'group90']]
'''




selected_rows = []
time_intervals = [
    pd.to_datetime('09:00').time(),
    pd.to_datetime('12:00').time(),
    pd.to_datetime('15:00').time(),
    pd.to_datetime('17:00').time(),
    pd.to_datetime('19:00').time(),
    pd.to_datetime('22:00').time()
]

def get_cycle(curr_time):
    for i, interval in enumerate(time_intervals, start=1):
        if curr_time < interval:
            return i
    return 7  # If the time is greater than 22:00


i = 0;
n = df_linreg_prices['id_data_updated'].nunique()

for station_idx, group in df_linreg_prices.groupby('id_data_updated'):
    grouped_by_date = group.groupby('date')
    
    print(station_idx) 

    for date, group2 in grouped_by_date:
        first = group2.iloc[0]
        first_time = first['timestamp'].time()
        first_cycle = get_cycle(first_time)

        stack_empty = True
        first_done = False

        for i in range(1, len(group2)):
            prev = group2.iloc[i - 1]
            curr = group2.iloc[i]
            curr_time = curr['timestamp'].time()
            cycle = get_cycle(curr_time)

            if curr['price'] > prev['price']:
                if stack_empty:
                    stack_empty = False
                    df_linreg_prices.loc[curr.name, 'change'] = curr['price'] - prev['price']
                    df_linreg_prices.loc[curr.name, 'bool_cycle_begin'] = 1
                    df_linreg_prices.loc[curr.name, 'cycle'] = cycle
                    selected_rows.append(df_linreg_prices.loc[curr.name])
                    first_done = True

                else:
                    df_linreg_prices.loc[curr.name, 'change'] = curr['price'] - prev['price']
                    df_linreg_prices.loc[curr.name, 'bool_cycle_begin'] = 0
                    df_linreg_prices.loc[curr.name, 'cycle'] = cycle
                    selected_rows.append(df_linreg_prices.loc[curr.name])

                    
            elif curr['price'] < prev['price']:
                stack_empty = True
                if not first_done:
                    df_linreg_prices.loc[first.name, 'change'] = 0
                    df_linreg_prices.loc[first.name, 'bool_cycle_begin'] = 1
                    df_linreg_prices.loc[first.name, 'cycle'] = first_cycle
                    selected_rows.append(df_linreg_prices.loc[first.name])
                    first_done = True



selected_df = pd.DataFrame(selected_rows)
selected_df['dow'] = selected_df['timestamp'].dt.day_name()

selected_df.reset_index(drop=True, inplace=True)

selected_df['brand_id'] = selected_df['id_data_updated'].map(df_char.set_index('id_data_updated')['brand_id'])
selected_df['date'] = selected_df['timestamp'].dt.date
selected_df['time'] = selected_df['timestamp'].dt.time

selected_df['cycle'] = selected_df['cycle'].astype(int)
selected_df['bool_cycle_begin'] = selected_df['bool_cycle_begin'].astype(int)

selected_df = selected_df.drop(['timestamp', 'date'], axis=1)
selected_df = selected_df[['id_data_updated', 'time', 'dow', 'brand_id', 'price', 'change', 'cycle', 'bool_cycle_begin', 'group80', 'group85', 'group90']]



print(selected_df)


selected_df.to_csv('test2.csv', index=False)
print('Saved!')
