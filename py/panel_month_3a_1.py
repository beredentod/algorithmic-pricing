import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime

from functions_1 import df_linreg_prices
from functions_1 import df_char

import stations_colors as sc


df_linreg_prices = df_linreg_prices.merge(df_char[['id_data_updated', 'brand_id']], on='id_data_updated', how='left')

df_linreg_prices['timestamp'] = pd.to_datetime(df_linreg_prices['timestamp'])
df_linreg_prices['date'] = df_linreg_prices['timestamp'].dt.date


grouped = df_linreg_prices.groupby('brand_id')

companies = ['aral', 'shell', 'total', 'esso', 'agip', 'avia', 'omv', 'jet', 'allguth']

means = {}

for brand, group in grouped:
	if brand in companies:
		grouped2 = group.groupby('date')

		means_array = []

		for date, g in grouped2:
			mean = g['price'].mean()
			means_array.append(mean)
			#print(g)

		means[brand] = means_array


rangeX = pd.date_range(start='2022-10-01', end='2022-10-31', freq='D')		
rangeX = rangeX.to_numpy()

# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


for brand, array in means.items():

	fmt = '-'

	if brand == 'jet' or brand == 'avia':
		fmt = '--'

	if brand == 'total':
		fmt = '-.'

	if brand == 'allguth':
		fmt = ':'

	ax.plot_date(rangeX, array, fmt=fmt, label=brand, color=sc.hex_to_rgb(sc.colors_brands[brand]))

#for index, row in df_prices.iterrows():
	#ax.plot_date(rangeX, row.values, fmt='-', label=fcs.lookUpAddress(index, True))

#ax.plot_date(rangeX, df_prices.mean().values, fmt='-', label='AVERAGE', zorder = 100, linewidth=3, color='black')


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%d-%b')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
#low = 1.7875
#high = 2.2215
#ax.set_ylim(low, high)

ax.set_xlim(datetime.date(2022, 10, 1), datetime.date(2022, 10, 31))


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title(f'Munich: Price level in October 2022')
ax.legend(loc="upper right", ncol=1)


# display the plot
plt.show()

# save figure to a file
save_name = f'./samples/MUC_Oct_2022.png'
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)
