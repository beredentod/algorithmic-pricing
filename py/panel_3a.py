import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
import stations_colors as sc

plt.rcParams.update({'font.size': 18})

#from compilation_peaks_2b import df_prices_ts as df_prices
#import compilation_peaks_2b as compilation
import functions_1 as fcs


#date = compilation.date
#param = compilation.param
#arg = compilation.arg

date = datetime(2022, 10, 3)
param = 'brand_id'
arg = 'aral'

#df_stations = fcs.selectStationsbyCategory(date, param, arg)
#df_prices = fcs.selectPriceRowsDate(date, df_stations)
#df_prices = fcs.trimToTimeSeries(df_prices)


save_name = f'./samples/MUC_{param}_{arg}_{date.date()}.png'


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

(df_stations, df_prices) = fcs.selectStationsbyCategoryRange(datetime(2022, 10, 1), datetime(2022, 10, 31), 'brand_id', 'aral')
df_prices = fcs.trimToTimeSeries(df_prices)

datetime_array = [datetime.combine(date, t) for t in df_prices.columns]
datetime_index = pd.DatetimeIndex(datetime_array)

rangeX = datetime_index.to_numpy()


companies = ['aral', 'shell', 'esso', 'total', 'jet', 'omv', 'avia']

for brand in companies:
	(df_stations, df_prices) = fcs.selectStationsbyCategoryRange(datetime(2022, 10, 1), datetime(2022, 10, 31), 'brand_id', brand)
	df_prices = fcs.trimToTimeSeries(df_prices)

	fmt = '-'

	if brand == 'jet' or brand == 'avia' or brand == 'raiffeisen':
		fmt = '--'

	if brand == 'total':
		fmt = '-.'

	if brand == 'star':
		fmt = ':'

	ax.plot_date(rangeX, df_prices.mean().values, fmt=fmt, label=brand, color=sc.hex_to_rgb(sc.colors_brands[brand]))



#for index, row in df_prices.iterrows():
#	ax.plot_date(rangeX, row.values, fmt='-', label=fcs.lookUpAddress(index, True))

#ax.plot_date(rangeX, df_prices.mean().values, fmt='-', label='AVERAGE', zorder = 100, linewidth=3, color='black')


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.895
high = 2.135
ax.set_ylim(low, high)
#ax.set_xlim(datetime.time(6,0), datetime.time(22,55))


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title(f'Munich: \'{param}\': {arg}, date: {date.date()}')

lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=7)

#box = ax.get_position()
#ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

ax.margins(x=0)


# display the plot
plt.tight_layout()
plt.show()

# save figure to a file
fig.savefig(save_name, dpi = 150, bbox_extra_artists=(lgd,), bbox_inches='tight')
print('Saved: ' + save_name)
