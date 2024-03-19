import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
plt.rcParams.update({'font.size': 18})
import matplotlib
import pandas as pd
import datetime
import stations_colors as sc
import numpy as np

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char


#import sys
#if len(sys.argv) != 2:
#    print("Usage: python script.py <value>")
#    sys.exit(1)

#brand = sys.argv[1]


brand = 'aral'

#day = datetime(2022, 10, 1).date()
#print(day)

df_price_inc['time'] = pd.to_datetime(df_price_inc['time'], format='%H:%M:%S')
df_price_inc.set_index('time', drop=False, inplace=True)


df_price_inc = df_price_inc[(df_price_inc['brand_id'] == brand)] #filter by brand

id_station = '60c3a07c-2ebe-4073-adae-a667e22fd4c8'
df_price_inc = df_price_inc[(df_price_inc['id_data_updated'] == id_station)]


#df_price_inc = df_price_inc.loc[(df_price_inc['date'] == day)]
#df_price_inc_corr = df_price_inc[(df_price_inc['bool_cycle_begin'] == 1)] #exclude increases within cycle
df_price_inc_corr = df_price_inc[(df_price_inc['change'] > 0.015)] #exclude those that have chnages lower than 1.5 cent
df_price_inc_6hour = df_price_inc[(df_price_inc['change'] == 0)] #include those that begin at 6am

df_price_inc = pd.concat([df_price_inc_corr, df_price_inc_6hour], ignore_index=True)


n = df_price_inc['id_data_updated'].nunique()
print(f'# of {brand} stations: {n}')

full = n * 31 # stations * days in the period (month)


# Create a range of 5-minute intervals between '6:00' and '22:50'
time_range = pd.date_range(start='2024-01-01 06:00', end='2024-01-01 22:55', freq='5min')
time_range = time_range.strftime('%H:%M') # Extract just the time (without dates)

# Assuming df_price_inc is your DataFrame with a 'time' column
# If 'time' column isn't in datetime format, convert it
df_price_inc['time'] = pd.to_datetime(df_price_inc['time'])

# Extract the time part (without dates) from the 'time' column
df_price_inc['time_without_date'] = df_price_inc['time'].dt.strftime('%H:%M')

# Count occurrences of each time within the specified range
occurrences = df_price_inc[df_price_inc['time_without_date'].isin(time_range)]['time_without_date'].value_counts().sort_index()

# Fill in missing times with zero occurrences
occurrences = occurrences.reindex(time_range, fill_value=0)

# normalize by the number of stations * days in the period (month)
occurrences = occurrences / full

print(occurrences)


# just for visulas - shift one period before to put the label of the bar chart behind the bar
occurrences = occurrences.reindex(['05:55'] + occurrences.index.tolist()).shift(periods=-1)


fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


# Plotting the bar chart using the adjusted x-axis positions and 'align=edge'
ax.bar(range(len(occurrences)), occurrences, color=sc.hex_to_rgb(sc.colors_brands[brand]), width=1, edgecolor='black', zorder=3, align='edge')

#occurrences.plot(kind='bar', color=sc.hex_to_rgb(sc.colors_brands[brand]), width=1, edgecolor='black', ax=ax, zorder=3, align='edge') 
ax.set_title('Price increases in DE in Oct 2022, '+brand+', by hours, price increases higher than 1.5ct only')
ax.set_xlabel('Time')
ax.set_ylabel('Share')

#ax.set_ylim(0, 0.18)

ax.grid(zorder=0)

# Set x-axis ticks at 1-hour intervals
hourly_ticks = pd.date_range(start=df_price_inc['time'].min().replace(minute=0), end=df_price_inc['time'].max().replace(minute=0), freq='2H')
hourly_ticks = hourly_ticks.strftime('%H:%M').tolist()

ax.set_xticks([occurrences.index.get_loc(t) for t in hourly_ticks])
ax.set_xticklabels(hourly_ticks, rotation=0)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

plt.tight_layout()


# display the plotl
#plt.show()


#save_name = 'test6'
#save_name = f'./samples/histograms/histogram_MUC_'+brand+'_'+day.strftime('%d%b%Y')+'_price_inc_Oct_22_no-corrections.png'
save_name = f'./samples/histogram_'+brand+'_DE_price_inc_10_2022-no_price_corrections.png'

# save figure to a file
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)
