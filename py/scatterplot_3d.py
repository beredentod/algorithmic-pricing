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

#print(df_daily_station_linreg)

means_all = df_daily_station_linreg['price_mean'].mean()
#dic['aggregate'] = means_all

for brand in big_oil:

	df_local = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	
	means_brand = df_local['price_mean'].mean()
	dic[brand] = means_brand - means_all

	#print(means_all - means_brand)

df_other = df_daily_station_linreg[~df_daily_station_linreg['brand_id'].isin((smaller_integrated + big_oil))]
mean_other = df_other['price_mean'].mean()
dic['non-integrated'] = mean_other - means_all


# set the figure and axis
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1)


for brand, val in dic.items():
	ax.plot(0, val, 'o', color = sc.hex_to_rgb(sc.colors_brands[brand]))
	ax.annotate(brand, (0.003, val-0.00047))

ax.axhline(y=0, color='black', linestyle='-')

# setting the axes labels and legend
ax.set_ylabel('Deviation from the mean price in Euro')
ax.set_xticks([])
#ax.set_title(f'Munich: cluster: \'{cluster}\', date: {start_date.date()} -- {end_date.date()}')

ax.spines[['right', 'bottom', 'top']].set_color('none')

plt.subplots_adjust(left=0.4, right=0.7, top=0.9, bottom=0.1)


# display the plot
#plt.show()

# save file
savefile = './samples/scatterplot_dev_mean_brand_all-DE.png'
fig.savefig(savefile, dpi = 150)
print('Saved: ' + savefile)