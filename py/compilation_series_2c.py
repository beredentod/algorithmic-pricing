from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
from functions_1 import df_linreg_prices
from functions_1 import df_char


single_date = datetime(2022, 10, 5)
param = 'id_data_updated'
arg = 'fb79c457-543a-4ff6-ba70-cd270ac2110a'




df_linreg_prices['timestamp'] = pd.to_datetime(df_linreg_prices['timestamp'])
df_linreg_prices['date'] = pd.to_datetime(df_linreg_prices['timestamp'].dt.date)


print(df_linreg_prices)

'''
df_filter = df_linreg_prices.loc[(df_linreg_prices['id_data_updated'] == arg) & (df_linreg_prices['date'] == single_date)]


print(df_filter)


selected_df = pd.DataFrame(columns=df_filter.columns)
selected_rows = []


stack_empty = True
first_done = False

for i in range(1, len(df_filter)):
	prev = df_filter.iloc[i-1]
	curr = df_filter.iloc[i]
	first = df_filter.iloc[0]

	if curr['price'] > prev['price']:

		if stack_empty == True:
			stack_empty = False
			selected_rows.append(curr)
			first_done = True

		else:
			print('Increase: ' + str(curr['price']))

	elif curr['price'] < prev['price']:
		stack_empty = True
		print('Decrease: ' + str(curr['price']))

		if first_done == False:
			selected_rows.append(first)
			first_done = True

	else:
		print('Stable: ' + str(curr['price']))

selected_df = pd.concat(selected_rows, axis=1).T
selected_df.reset_index(drop=True, inplace=True)

print(selected_df)
'''	


selected_rows = []


grouped_by_station = df_linreg_prices.groupby('id_data_updated')

for _, group in grouped_by_station:
	grouped_by_date =  group.groupby('date')

	for date, group2 in grouped_by_date:

		stack_empty = True
		first_done = False

		for i in range(1, len(group2)):
			prev = group2.iloc[i-1]
			curr = group2.iloc[i]
			first = group2.iloc[0]

			if curr['price'] > prev['price']:

				if stack_empty == True:
					stack_empty = False
					selected_rows.append(curr)
					first_done = True

				#else:
				#	print('Increase: ' + str(curr['price']))

			elif curr['price'] < prev['price']:
				stack_empty = True
				if first_done == False:
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

selected_df = selected_df[['id_data_updated', 'date', 'time', 'dow', 'brand_id', 'price', 'group80', 'group85', 'group90']]


print(selected_df)


selected_df.to_csv('price-increases_MUC_Oct22.csv', index=False)
print('Saved!')