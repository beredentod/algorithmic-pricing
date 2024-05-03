import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

import stations_colors as sc
from compilation_first_mover_events_2h import df_brands 

# subtract 100% to get the extra margin
df_brands['percent'] = df_brands['margin_first-movership'] - 1 

# sorting
df_brands = df_brands.sort_values(by=['percent'], ascending=False)



# make font bigger in the generated picture
plt.rcParams.update({'font.size': 18})

# set the figure and axis
fig, ax = plt.subplots(figsize=(16, 9))

# generate the plot
bars = ax.bar(df_brands['brand_id'], df_brands['percent'])

# rotate the label for each bar, as they overlap
plt.xticks(rotation=45, ha='right')

# add the 0% line 
ax.axhline(y=0, color='k')

# format to display %
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

# set the color of each bar to the brand's color
for index, value in enumerate(df_brands['brand_id']):
    bars[index].set_color(sc.hex_to_rgb(sc.colors_brands[value]))

# set title of the graph
ax.set_title('Germany: Margin of being the first mover in cluster, Oct 2022')

#plt.show()
plt.tight_layout()

# save file
savefile = './samples/barchart_firstmovership_margin.png'
fig.savefig(savefile, dpi = 150)
print('Saved: ' + savefile)