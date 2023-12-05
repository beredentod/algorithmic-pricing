import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import pandas as pd
import datetime
import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char


brand = 'shell'
#day = datetime(2022, 10, 1).date()
#print(day)


# set time format
df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc.set_index('time', drop=False, inplace=True)


## filters ##

df_price_inc = df_price_inc[(df_price_inc['brand_id'] == brand)] #filter by brand

#df_price_inc = df_price_inc.loc[(df_price_inc['date'] == day)]
df_price_inc_corr = df_price_inc[(df_price_inc['bool_cycle_begin'] == 1)] #exclude increases within cycle
df_price_inc_corr = df_price_inc[(df_price_inc['change'] > 0.015)] #exclude those that have chnages ower than 1.5 cent
df_price_inc_6hour = df_price_inc[(df_price_inc['change'] == 0)] #include those that begin at 6am

df_price_inc = pd.concat([df_price_inc_corr, df_price_inc_6hour], ignore_index=True)


## generate results ##

results = df_price_inc.groupby('cycle').size()


rangeX = ['6h', '9h', '12h', '15h', '17h', '19h', '22h']
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
	bars[index].set_color(sc.hex_to_rgb(sc.colors_brands[brand]))


ax.set_xlabel('Cycle during day')
ax.set_ylabel('Frequency')
ax.set_title('Price increases (cycle begin) in MUC in Oct 2022, '+brand+', bundled by cycles, without 1ct increases')
#ax.set_title('Price increases (cycle begin) in MUC in Oct 2022, '+brand+', '+day.strftime('%d%b%Y')+', by hours, without 1ct increases')
#plt.title('Price increases (cycle begin) in MUC in Oct 2022, by hours, without 1ct increases')

# display the plot
plt.show()


#save_name = f'./samples/histograms/bar_chart_MUC_'+brand+'.png'

# save figure to a file
#fig.savefig(save_name, dpi = 150)
#print('Saved: ' + save_name)


