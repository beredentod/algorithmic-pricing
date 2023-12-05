import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd

import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_price_inc


brand = 'shell'
#day = datetime(2022, 10, 1).date()


#save_name = f'./samples/histograms/histogram_MUC_'+brand+'_'+day.strftime('%d%b%Y')+'_price_inc_Oct_22_no-corrections.png'


df_prices_inc = df_price_inc[(df_price_inc['brand_id'] == 'shell') & (df_price_inc['cycle_leader'] == 1)]


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc.set_index('time', drop=False, inplace=True)


ax = df_price_inc['time'].hist(bins=204, edgecolor='black', color=sc.hex_to_rgb(sc.colors_brands[brand]))
#ax = df_price_inc['time'].hist(bins=204, edgecolor='black')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))


ax.set_xlabel('Time')
ax.set_ylabel('Frequency')
ax.set_title('Price leaders per day per cluster per cycle in MUC in Oct 2022, '+brand)
#plt.title('Price increases (cycle begin) in MUC in Oct 2022, by hours, without 1ct increases')


# display the plot
plt.show()

# save figure to a file
#fig.savefig(save_name, dpi = 150)
#print('Saved: ' + save_name)
