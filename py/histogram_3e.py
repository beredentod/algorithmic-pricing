import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib
import pandas as pd
import datetime
import stations_colors as sc
import numpy as np

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char


#brand = 'shell'
#cluster = 'group90'
#import sys
#cluster_no = int(sys.argv[1])



#for index, rows in df_price_inc.iterrows():
#	print(rows['date'])


#import sys
#id_data_updated = str(sys.argv[1])

#brand = df_char.at[df_char[df_char['id_data_updated'] == id_data_updated].index[0], 'brand_id']

brand = 'shell'
#day = datetime(2022, 10, 1).date()
#print(day)

df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc.set_index('time', drop=False, inplace=True)


df_price_inc = df_price_inc[(df_price_inc['brand_id'] == brand)] #filter by brand

n = df_price_inc['id_data_updated'].nunique()

print(f'# of {brand} stations: {n}')

full = n * 31

#df_price_inc = df_price_inc.loc[(df_price_inc['date'] == day)]
df_price_inc_corr = df_price_inc[(df_price_inc['bool_cycle_begin'] == 1)] #exclude increases within cycle
df_price_inc_corr = df_price_inc[(df_price_inc['change'] > 0.015)] #exclude those that have chnages lower than 1.5 cent
df_price_inc_6hour = df_price_inc[(df_price_inc['change'] == 0)] #include those that begin at 6am


df_price_inc = pd.concat([df_price_inc_corr, df_price_inc_6hour], ignore_index=True)


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


#ax = df_price_inc['time'].hist(bins=204, edgecolor='black', color=sc.hex_to_rgb(sc.colors_brands[brand]))

df_price_inc['time_num'] = df_price_inc['time'].dt.hour * 60 + df_price_inc['time'].dt.minute

# Compute the histogram using numpy
hist_values, bin_edges = np.histogram(df_price_inc['time_num'], bins=204)

hist_values = hist_values / full


ax.bar(bin_edges[:-1], hist_values, width=(bin_edges[1] - bin_edges[0]), edgecolor='black', color=sc.hex_to_rgb(sc.colors_brands[brand]))
ax.set_xlabel('Time')
ax.set_ylabel('Frequency')
#plt.title('Histogram of Time')

# Set specific x-axis ticks and labels
specific_times = [6 * 60, 9 * 60, 12 * 60, 15 * 60, 17 * 60, 19 * 60, 22 * 60]
labels = ['6:00', '9:00', '12:00', '15:00', '17:00', '19:00', '22:00']

ax.set_xticks(specific_times)
ax.set_xticklabels(labels)

ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.show()


#df_price_inc = df_price_inc[(df_price_inc['cycle_leader80'] == 1)]
#df_price_inc = df_price_inc[(df_price_inc['mult_leader80'] == 0)]

#ax = df_price_inc['time'].hist(bins=204, edgecolor='black', color='red')
'''


#ax = df_price_inc['time'].hist(bins=204, edgecolor='black')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))


#ax.set_ylim(ymin = 0, ymax = 600)


ax.set_xlabel('Time')
ax.set_ylabel('Frequency')
ax.set_title('Price increases (cycle begin) in MUC in Oct 2022, '+brand+', cycle_leader80 = 1, by hours, without 1ct increases')
#ax.set_title('Price increases (cycle begin) in MUC in Oct 2022, '+brand+', '+day.strftime('%d%b%Y')+', by hours, without 1ct increases')
#plt.title('Price increases (cycle begin) in MUC in Oct 2022, by hours, without 1ct increases')

# display the plot
plt.show()


#save_name = f'./samples/histograms/histogram_MUC_'+brand+'_'+day.strftime('%d%b%Y')+'_price_inc_Oct_22_no-corrections.png'
#save_name = f'./samples/histogram_MUC_price_inc_Oct_22_no-corrections.png'
save_name = 'test6'

# save figure to a file
#fig.savefig(save_name, dpi = 150)
#print('Saved: ' + save_name)'''
