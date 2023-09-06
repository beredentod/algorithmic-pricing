import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

from compilation import df_reg_results


coefficients = df_reg_results['Coefficient'] # the calculated coefficients 
errors = [df_reg_results['Coefficient'] - df_reg_results['Lower CI'], df_reg_results['Upper CI'] - df_reg_results['Coefficient']]

	
# Set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


# Set the labels to index names
x_labels = df_reg_results.index

ax.errorbar(coefficients, x_labels, xerr=errors, linestyle='None', marker='None', markeredgecolor='k', ecolor='k')	


# Set the labels and title
ax.set_ylabel('Variables')
ax.set_xlabel('Coefficient')
ax.set_title('Regression Results, group90')


#ax.legend(loc='right')

#ax.axis(xmin=1.93,xmax=2.005)

# Display the plot
plt.show()