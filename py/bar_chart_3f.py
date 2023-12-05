import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd

import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_price_inc


cluster = 90

#sel_clusters = [1, 6, 10, 15, 16, 22]

# Filtering rows with specified values in 'cluster90' column
#df_price_inc = df_price_inc[df_price_inc['group'+str(cluster)].isin(sel_clusters)]


df_price_inc = df_price_inc[df_price_inc['mult_leader'+str(cluster)] == 0] #filter mult leaders

df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc['time'] = df_price_inc['time'].dt.time
#print(df_price_inc['time'].unique())
#df_price_inc = df_price_inc[(df_price_inc['time']>= pd.to_datetime('09:00').time()) & (df_price_inc['time'] < pd.to_datetime('22:00').time())]


results = df_price_inc[df_price_inc['cycle_leader'+str(cluster)] == 1].groupby('brand_id').size().sort_values(ascending=False)


rangeX = results.index # names of the brands
rangeY = results.values # values = number of stations per brand


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

# generate the plot
bars = ax.bar(rangeX, rangeY)


#rotate the label for each bar, as they overlap
plt.xticks(rotation=45, ha='right')
ax.bar_label(bars)


# set the color of each bar to the brand's color
for index, value in enumerate(rangeY):
	bars[index].set_color(sc.hex_to_rgb(sc.colors_brands[rangeX[index]]))


# set title of the graph
ax.set_title('Price leader per day per cluster (group '+str(cluster)+') per cycle, just cluters: '+str(sel_clusters)+', just between 9:00 and 21:55, no multiple leaders, Munich Oct 2022')
#ax.set_title('Price leader per day per cluster (group '+str(cluster)+') per cycle, filtered out: cluters: '+str(exclude_sel_clusters)+', just between 9:00 and 21:55, no multiple leaders, Munich Oct 2022')

plt.show()

# save file
savefile = './samples/barchart_price_leaders_MUC_Oct2022_group'+str(cluster)+'_no_mult_leaders_9:00-21:55_only-sel_clusters'+str(sel_clusters)+'.png'
fig.savefig(savefile, dpi = 150)
print('Saved: ' + savefile)
