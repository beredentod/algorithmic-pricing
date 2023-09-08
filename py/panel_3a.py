import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

from compilation_2 import df_prices_ts as df_prices
import compilation_2 as compilation
import functions_1 as fcs

date = compilation.date
param = compilation.param
arg = compilation.arg

save_name = f'./samples/MUC_{param}_{arg}_{date.date()}.png'


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


datetime_array = [datetime.combine(date, t) for t in df_prices.columns]
datetime_index = pd.DatetimeIndex(datetime_array)

rangeX = datetime_index.to_numpy()


for index, row in df_prices.iterrows():
	ax.plot_date(rangeX, row.values, fmt='-', label=fcs.lookUpAddress(index, True))

ax.plot_date(rangeX, df_prices.mean().values, fmt='-', label='AVERAGE', zorder = 100, linewidth=3, color='black')


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
ax.set_ylim(low, high)


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title(f'Munich: \'{param}\': {arg}, date: {date.date()}')
ax.legend(loc="lower center", ncol=4)


# display the plot
# plt.show()

# save figure to a file
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)
