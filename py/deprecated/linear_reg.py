import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd

#from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from stargazer.stargazer import Stargazer

import stations_colors as sc


df = pd.read_csv('../data/MUC_oct22_aggregate.csv')


print(unique)


'''
Y = df['P_it']
X = df[['dummy_Mon', 'dummy_Tue', 'dummy_Wed', 'dummy_Thu', 'dummy_Fri', 'dummy_Sat', 'dummy_Sun']]

model = sm.OLS(Y, X)
results = model.fit()

print(results.summary())

df_results = pd.DataFrame({
    'Coefficient': results.params,
    'Lower CI': results.conf_int().iloc[:, 0],
    'Upper CI': results.conf_int().iloc[:, 1]
})

# Set the coefficients and errors
coefficients = df_results['Coefficient'] # the calculated coefficients 
errors = [df_results['Coefficient'] - df_results['Lower CI'], df_results['Upper CI'] - df_results['Coefficient']]
'''
	



# Set the figure and axis
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(6, 5))
#ax = fig.add_subplot(1, 1, 1)


# Set the x-axis labels to 'Mon', 'Tue', 'Wed', ...
#x_labels = list(map(lambda x: x.replace('dummy_', ''), df_results.index))
x_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#ax.errorbar(coefficients, x_labels, xerr=errors, linestyle='None', marker='o', markeredgecolor='k', ecolor='k')	


# Set the labels and title
ax.set_ylabel('Variables')
ax.set_xlabel('Coefficient')
ax.set_title('Regression Results')
#ax.legend(loc='right')

#ax.axis(xmin=1.93,xmax=2.005)

# Display the plot
#plt.show()


#save_name = './samples/linreg_dow_MUC_oct22_comparison''.png'
#fig.savefig(save_name, dpi = 150)
#print('Saved: ' + save_name)

