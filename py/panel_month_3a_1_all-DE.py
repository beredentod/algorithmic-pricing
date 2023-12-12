import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime

import functions_1 as fcs
from functions_1 import df_daily_station_linreg

import stations_colors as sc

dic = {}

big_oil = ['aral', 'shell', 'esso', 'total', 'jet']
smaller_integrated = ['agip', 'hem', 'omv', 'star', 'avia', 'bft']

'''
for brand in big_oil:

	df = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	grouped = df.groupby('date')['price_mean'].mean()

	dic[brand] = grouped'''

'''
df_integ = df_daily_station_linreg[df_daily_station_linreg['brand_id'].isin(smaller_integrated)]
grouped = df_integ.groupby('date')['price_mean'].mean()
dic['other_integrated'] = grouped'''

for brand in smaller_integrated:

	df = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	grouped = df.groupby('date')['price_mean'].mean()

	dic[brand] = grouped

'''df_sonstige = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == 'sonstige']
grouped = df_sonstige.groupby('date')['price_mean'].mean()
dic['sonstige'] = grouped'''


df_other = df_daily_station_linreg[~df_daily_station_linreg['brand_id'].isin((smaller_integrated + big_oil))]
grouped = df_other.groupby('date')['price_mean'].mean()
dic['non-integrated'] = grouped


#print(dic)


rangeX = pd.date_range(start='2022-10-01', end='2022-12-31', freq='D')		
rangeX = rangeX.to_numpy()

# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)



for brand, array in dic.items():

	array = array.to_numpy()

	fmt = '-'

	if brand == 'jet' or brand == 'avia' or brand == 'raiffeisen':
		fmt = '--'

	if brand == 'total':
		fmt = '-.'

	if brand == 'star':
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

ax.set_xlim(datetime.date(2022, 10, 1), datetime.date(2022, 12, 31))


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title(f'Price level in Germany Oct-Dec 2022, smaller brands')
ax.legend(loc="upper right", ncol=1)


# display the plot
plt.show()


# save figure to a file
save_name = f'./samples/all-DE_Oct-Dec_2022__smaller-brands.png'
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)
