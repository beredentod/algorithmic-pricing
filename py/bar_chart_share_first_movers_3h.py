import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_share_first_movers


big_oil = ['aral', 'shell', 'total', 'esso', 'jet']
other_integr = ['agip', 'avia', 'bft', 'star', 'hem', 'omv']

brands = big_oil + other_integr + ['other']


data = []

for brand in brands:
    mean = df_share_first_movers[f'share_diff_{brand}'].mean()
    data.append({'brand': brand, 'mean': mean})

df_means = pd.DataFrame(data)

labels = (df_means['mean'] * 100).round(1).astype('str') + '%'

# set the figure and axis
fig, ax = plt.subplots(figsize=(16, 9))

# generate the plot
bars = ax.bar(df_means['brand'], df_means['mean'])

# rotate the label for each bar, as they overlap
plt.xticks(rotation=45, ha='right')

ax.axhline(y=0, color='k')

for container in ax.containers:
    ax.bar_label(container, labels=labels)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter()) 

# set the color of each bar to the brand's color
for index, value in enumerate(df_means['brand']):
    bars[index].set_color(sc.hex_to_rgb(sc.colors_brands[value]))


ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))


# set title of the graph
#ax.set_title('Germany: First movers per day per cluster (group '+str(cluster)+') per cycle, no clusters with aral or shell, NO simultaneous movers, Oct 2022')

plt.show()
plt.tight_layout()

# save file
#savefile = './samples/barchart_first_movers_all_10-2022_group'+str(cluster)+'_no-aral-no-shell_no-mult-leaders'+'.png'
#fig.savefig(savefile, dpi = 150)
#print('Saved: ' + savefile)