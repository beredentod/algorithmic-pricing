import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd

import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_char

plt.rcParams.update({'font.size': 18})


df_char = df_char.loc[(df_char['first'] <= datetime(2022, 10, 1)) & (df_char['last'] >= datetime(2022, 10, 31))]

n = len(df_char)
print(n)

grouped = df_char.groupby('brand_id').size().sort_values(ascending=False)

#grouped = (grouped / n).round(2) * 100 # market share
grouped = (grouped / n) * 100 # market share

big_oil = ['aral', 'shell', 'esso', 'total', 'jet']
smaller_integrated = ['agip', 'hem', 'omv', 'star', 'avia', 'bft']

agg = big_oil + smaller_integrated

categories_to_group = grouped[~grouped.index.isin(agg)]

# Sum values of categories not in array X and add to a new 'other' category
other_category_sum = categories_to_group.sum()

# Create a new DataFrame with the 'other' category
grouped_with_other = grouped.copy()
grouped_with_other = grouped_with_other[~grouped_with_other.index.isin(categories_to_group.index)]
grouped_with_other.loc['other'] = other_category_sum

grouped = grouped_with_other

grouped = grouped.round(1)

rangeX = grouped.index # names of the brands
rangeY = grouped.values # values = number of stations per brand

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
ax.set_title('German petrol stations by brand, Oct 2022')

plt.tight_layout()
#plt.show()


# save file
savefile = './samples/all_DE_barchart_by-brand.png'
fig.savefig(savefile, dpi = 150)
print('Saved: ' + savefile)

