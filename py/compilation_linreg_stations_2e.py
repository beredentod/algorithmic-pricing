import datetime
import pandas as pd
import numpy as np

import functions_1 as fcs
from functions_1 import df_linreg_prices



df_linreg_prices['timestamp'] = pd.to_datetime(df_linreg_prices['timestamp'])

df_linreg_prices['date'] = df_linreg_prices['timestamp'].dt.date
df_linreg_prices['time'] = df_linreg_prices['timestamp'].dt.time

'''
df_means = df_linreg_prices.groupby(['id_data_updated', 'date', 'group80'])['price'].mean().reset_index()
df_means.rename(columns={'price': 'price_mean'}, inplace=True)

new_df_17h = pd.DataFrame(columns=['id_data_updated', 'date', 'price_17h'])
new_df_18h = pd.DataFrame(columns=['id_data_updated', 'date', 'price_18h'])

grouped = df_linreg_prices.groupby('id_data_updated')
for id_data, group in grouped:
	
	grouped2 = group.groupby('time')

	for time, group2 in grouped2:

		if time == datetime.time(17, 0):	
		
			result_df_17h = pd.DataFrame({'id_data_updated': id_data,
				'date': group2['date'],
				'price_17h': group2['price']})

			new_df_17h = pd.concat([new_df_17h, result_df_17h], axis=0, join='outer', ignore_index=True)

		if time == datetime.time(18, 0):	
			result_df_18h = pd.DataFrame({'id_data_updated': id_data,
				'date': group2['date'],
				'price_18h': group2['price']})

			new_df_18h = pd.concat([new_df_18h, result_df_18h], axis=0, join='outer', ignore_index=True)


merged_df = pd.merge(df_means, new_df_17h, on=['id_data_updated', 'date'], how='inner')
merged_df = pd.merge(merged_df, new_df_18h, on=['id_data_updated', 'date'], how='inner')
'''



# Calculate mean price for each group ('id_data_updated', 'date', 'group80')
df_means = df_linreg_prices.groupby(['id_data_updated', 'date', 'group80'])['price'].mean().reset_index()
df_means.rename(columns={'price': 'price_mean'}, inplace=True)

# Filter data for time 17:00 and 18:00
new_df = df_linreg_prices[df_linreg_prices['time'].isin([datetime.time(17, 0), datetime.time(18, 0)])]

# Pivot data to create separate columns for price at 17:00 and 18:00
new_df = new_df.pivot(index=['id_data_updated', 'date'], columns='time', values='price').reset_index()
new_df.columns.name = None  # Remove the columns name from pivot

# Merge mean prices and prices at 17:00 and 18:00
merged_df = pd.merge(df_means, new_df, on=['id_data_updated', 'date'], how='inner')
merged_df.rename(columns={datetime.time(17, 0): 'price_17h', datetime.time(18, 0): 'price_18h'}, inplace=True)

# Display the optimized merged DataFrame
print(merged_df)
