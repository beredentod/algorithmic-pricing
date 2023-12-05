import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

from compilation_2 import df_reg_results_char as df_reg_results
from compilation_2 import df_reg_results_char as cluster


coefficients = df_reg_results['Coefficient'] # the calculated coefficients 
errors = [df_reg_results['Coefficient'] - df_reg_results['Lower CI'], df_reg_results['Upper CI'] - df_reg_results['Coefficient']]

	
# Set the figure and axis
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


# Set the labels to index names
x_labels = df_reg_results.index

ax.errorbar(coefficients, x_labels, xerr=errors, linestyle='None', marker='None', markeredgecolor='k', ecolor='k')	


# Set the labels and title
#ax.set_ylabel('Regression parameters')
ax.set_xlabel('Coefficient')
ax.set_title('MUC: Regression results for fixed effects in clusters, no monopolist clusters (HHi < 1)')


#ax.legend(loc='right')

ax.axis(xmin=-0.18,xmax=0.18)

plt.axvline(0, color='black')

# Display the plot
plt.show()

save_name = f'../plots/linreg/MUC_linreg_cluster_FE_parameters_no-monopolists.png'
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)


