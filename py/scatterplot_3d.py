import matplotlib.pyplot as plt
import pandas as pd

import compilation_2 as compilation

start_date = compilation.start_date
end_date = compilation.end_date
param = compilation.param
arg = compilation.arg
df_reg_results = compilation.df_reg_results
cluster = compilation.cluster


save_name = f'./samples/MUC_scatterplot_HHi_FE_{cluster}_{start_date.date()}_{end_date.date()}.png'


# set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

rangeX = df_reg_results['HHi']
rangeY = df_reg_results['Fixed effect']

ax.scatter(rangeX, rangeY)


# setting the axes labels and legend
ax.set_xlabel('Market concentration for cluster')
ax.set_ylabel('Fixed effect for cluster')
ax.set_title(f'Munich: cluster: \'{cluster}\', date: {start_date.date()} -- {end_date.date()}')
#ax.legend(loc="lower center", ncol=4)

low = 1.9
high = 2
ax.set_ylim(low, high)

# display the plot
#plt.show()

# save figure to a file
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)