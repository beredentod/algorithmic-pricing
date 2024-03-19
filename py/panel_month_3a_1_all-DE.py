import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams.update({'font.size': 18})
import pandas as pd
import numpy as np
import datetime

import functions_1 as fcs
from functions_1 import df_daily_station_linreg

import stations_colors as sc

dic = {}

big_oil = ['aral', 'shell', 'esso', 'total', 'jet']
smaller_integrated = ['agip', 'hem', 'omv', 'star', 'avia', 'bft']

print(df_daily_station_linreg)

means_all = df_daily_station_linreg.groupby('date')['price_mean'].mean()
#dic['aggregate'] = means_all

for brand in big_oil:

	df_local = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	
	means_brand = df_local.groupby('date')['price_mean'].mean()
	dic[brand] = means_brand - means_all

	print(brand + ': ' + str(dic[brand].max() - dic[brand].min()))

	#print(means_all - means_brand)

'''
df_integ = df_daily_station_linreg[df_daily_station_linreg['brand_id'].isin(smaller_integrated)]
grouped = df_integ.groupby('date')['price_mean'].mean()
dic['other_integrated'] = grouped
'''

'''
for brand in smaller_integrated:

	df = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	grouped = df.groupby('date')['price_mean'].mean()

	dic[brand] = grouped'''

'''df_sonstige = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == 'sonstige']
grouped = df_sonstige.groupby('date')['price_mean'].mean()
dic['sonstige'] = grouped'''


df_other = df_daily_station_linreg[~df_daily_station_linreg['brand_id'].isin((smaller_integrated + big_oil))]
mean_other = df_other.groupby('date')['price_mean'].mean()
dic['non-integrated'] = mean_other - means_all


#print(dic)


rangeX = pd.date_range(start='2022-10-01', end='2022-12-31', freq='D')		
rangeX = rangeX.to_numpy()

# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

ax.axhline(y=0, color='black', linestyle='-')

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


ax.set_ylim(-0.039, 0.039)
ax.set_xlim(datetime.date(2022, 10, 1), datetime.date(2022, 12, 31))


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title(f'Deviation of price level from day\'s mean, Germany, Oct-Dec 2022, big oil')
#ax.legend(loc="upper right", ncol=1)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=6)



# display the plot
#plt.show()
plt.tight_layout()


# save figure to a file
save_name = f'./samples/dev-mean_all-DE_Oct-Dec_2022_big_oil.png'
fig.savefig(save_name, dpi = 150, bbox_extra_artists=(lgd,), bbox_inches='tight')
print('Saved: ' + save_name)
