import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

from compilation import df_prices


save_name = './samples/agip_stations_MUC_01oct2022.png'


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

date = datetime(2022,10,1)


datetime_array = [datetime.combine(date, t) for t in df_prices.columns[1:]]
datetime_index = pd.DatetimeIndex(datetime_array)


rangeX = datetime_index.to_numpy()

print(rangeX)



for index, row in df_prices.iterrows():
	ax.plot_date(rangeX, row[1:].values, fmt='-', label=row['id_data'])


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
ax.set_ylim(low, high)


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title('Munich: AVG prices across brands on '+ str(date.date()))
ax.legend(loc="lower center", ncol=3)


# display the plot
plt.show()

# save figure to a file
#fig.savefig(save_name, dpi = 150)
#print('Saved: ' + save_name)