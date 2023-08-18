import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

#from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.formula.api import ols
from stargazer.stargazer import Stargazer

import stations_colors as sc


df_agg = pd.read_csv('../data/MUC_oct22_timestamps-dummies_aggregate.csv')

#company = input('company: ')

brands = ['aral', 'shell', 'agip', 'esso', 'jet', 'omv', 'allguth', 'total', 'avia']


#company = 'aggregate'

# Set the figure and axis
#fig, ax = plt.subplots()
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


# Set the x-axis labels to 'Mon', 'Tue', 'Wed', ...
#x_labels = list(map(lambda x: x.replace('dummy_', ''), df_results.index))

rangeX = (pd.date_range("6:00", "22:50", freq="5min")).to_numpy()

# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


for company in brands:
	df = df_agg[df_agg['brand'].str.contains(company)]

	Y = df['P_it']
	dummy = df['timestamp']

	# Add a constant term to the dummy variable
	X = sm.add_constant(dummy)

	fit = ols('P_it ~ C(timestamp)', data=df).fit() 
	print(fit.summary())

	df_results = pd.DataFrame({'Coefficient': fit.params})

	intercept = df_results.loc['Intercept', 'Coefficient']

	df_results = df_results.add(intercept)
	df_results = df_results.drop('Intercept')

	print(df_results)

	if company == 'jet' or company == 'avia' or company == 'omv':
		ax.plot(rangeX, df_results['Coefficient'], color=sc.hex_to_rgb(sc.colors_brands[company]), linestyle='--', label=company)
	elif company == 'total':
		ax.plot(rangeX, df_results['Coefficient'], color=sc.hex_to_rgb(sc.colors_brands[company]), linestyle='-.', label=company)
	elif company == 'allguth':
		ax.plot(rangeX, df_results['Coefficient'], color=sc.hex_to_rgb(sc.colors_brands[company]), linestyle=':', label=company)	
	else:
		ax.plot(rangeX, df_results['Coefficient'], color=sc.hex_to_rgb(sc.colors_brands[company]), label=company)



#ax.errorbar(x_labels, coefficients, yerr=errors, linestyle='-', marker='None')	



# Set the labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Price in Euro')
ax.set_title('Regression results in regards to time – Comparison')
#ax.legend(loc='right')

# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
#ax.set_ylim(low, high)
ax.legend(loc="upper right")

#ax.axis(xmin=1.93,xmax=2.005)

# Display the plot
#plt.show()

save_name = './samples/linreg_timestamps_MUC_oct22_comparison.png'
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)

