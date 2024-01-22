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

import sys
if len(sys.argv) != 2:
    print("Usage: python script.py <value>")
    sys.exit(1)

brand = sys.argv[1]



#brand = 'aral'

#day = datetime(2022, 10, 1).date()
#print(day)

#unique_df1 = df_char[df_char['brand_id'] == brand]['id_data_updated'].tolist()
#unique_df2 = df_price_inc[df_price_inc['brand_id'] == brand]['id_data_updated'].unique().tolist()

#print([value for value in unique_df1 if value not in unique_df2])


df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc.set_index('time', drop=False, inplace=True)

df_price_inc = df_price_inc[(df_price_inc['brand_id'] == brand)] #filter by brand

#df_price_inc = df_price_inc.loc[(df_price_inc['date'] == day)]
#df_price_inc_corr = df_price_inc[(df_price_inc['bool_cycle_begin'] == 1)] #exclude increases within cycle
df_price_inc_corr = df_price_inc[(df_price_inc['change'] > 0.015)] #exclude those that have chnages lower than 1.5 cent
df_price_inc_6hour = df_price_inc[(df_price_inc['change'] == 0)] #include those that begin at 6am

df_price_inc = pd.concat([df_price_inc_corr, df_price_inc_6hour], ignore_index=True)

n = df_price_inc['id_data_updated'].nunique()
print(f'# of {brand} stations: {n}')
full = n * 31

#print(df_price_inc)


# Count occurrences of each time within the specified range
occurrences = df_price_inc['cycle'].value_counts().sort_index()

occurrences = occurrences.reindex(range(1, 8), fill_value=0)

occurrences = occurrences / full


print(occurrences)

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

occurrences.plot(kind='bar', color=sc.hex_to_rgb(sc.colors_brands[brand]), edgecolor='black', ax=ax) 

ax.set_title('Price increases in DE in Oct 2022, '+brand+', aggregated in cycles, price increases higher than 1.5ct only')
ax.set_xlabel('Cycle')
ax.set_ylabel('Share')

ticks = ['6:00', '9:00', '12:00', '15:00', '17:00', '19:00', '22:00']

ax.set_xticklabels(ticks, rotation=0)

ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

# display the plotl
#plt.show()


#save_name = 'test6'
#save_name = f'./samples/histograms/histogram_MUC_'+brand+'_'+day.strftime('%d%b%Y')+'_price_inc_Oct_22_no-corrections.png'
save_name = f'./samples/bar_chart_'+brand+'_DE_price_inc_cycles-agg_10_2022.png'

# save figure to a file
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)
