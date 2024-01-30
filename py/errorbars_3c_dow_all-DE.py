import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
import pandas as pd

import functions_1 as fcs
from functions_1 import df_daily_station_linreg as df

import stations_colors as sc


ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ordered_days = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
#ordered_days = reversed(ordered_days)

dic = {}

big_oil = ['aral', 'shell', 'esso', 'total', 'jet']
smaller_integrated = ['agip', 'hem', 'omv', 'star', 'avia', 'bft']

df['date'] = pd.to_datetime(df['date'])
df['dow'] = df['date'].dt.day_name()

'''
df = df[df['brand_id'] == 'esso']
grouped = df.groupby('dow')['price_mean'].mean().sort_values()

print(grouped)'''


grouped = df.groupby('dow')['price_mean'].mean()
grouped.index = pd.Categorical(grouped.index, categories=ordered_days, ordered=True)
grouped = grouped.sort_index()
mean = df['price_mean'].mean()
dic['aggregate'] = (grouped - mean) * 100
#dic['aggregate'] = grouped #abs val


for brand in big_oil:

	df_filter = df[df['brand_id'] == brand]
	grouped = df_filter.groupby('dow')['price_mean'].mean()
	grouped.index = pd.Categorical(grouped.index, categories=ordered_days, ordered=True)
	grouped = grouped.sort_index()
	mean = df_filter['price_mean'].mean()

	dic[brand] = (grouped - mean) * 100 #deviation
	#dic[brand] = grouped #abs val

	
# Set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)

#print(dic)


# Set the labels to index names
#variables = df_reg_results.index


for brand, array in dic.items():
	fmt = '-'
	width = 1

	if brand == 'jet' or brand == 'avia' or brand == 'raiffeisen':
		fmt = '--'

	if brand == 'total':
		fmt = '-.'

	if brand == 'star':
		fmt = ':'

	if brand == 'aggregate' or brand == 'jet' or 'total':
		width = 2

	ax.errorbar(array.values, array.index, fmt=fmt, linewidth=width, label=brand, color=sc.hex_to_rgb(sc.colors_brands[brand]))	


# Set the labels and title
#ax.set_ylabel('Regression parameters')
ax.set_xlabel('Price in Euro')
ax.set_title('Deviation of price level from the brand\'s mean, by day of the week')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=6)

ax.axis(xmin=-1.2,xmax=1.2)
plt.axvline(0, color='black')

# Display the plot
#plt.show()
plt.tight_layout()


save_name = f'./samples/dev-mean_all-DE_dow.png'
fig.savefig(save_name, dpi = 150, bbox_extra_artists=(lgd,), bbox_inches='tight')
print('Saved: ' + save_name)

