import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
import pandas as pd

from compilation_2h_linreg_cluster_char import df_reg_results_char as df_reg_results
from compilation_2h_linreg_cluster_char import df_reg_results_char as cluster


coefficients = df_reg_results['Coefficient'] # the calculated coefficients 
errors = [df_reg_results['Coefficient'] - df_reg_results['Lower CI'], df_reg_results['Upper CI'] - df_reg_results['Coefficient']]

	
# Set the figure and axis
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1)

#dic = {'n' : 'number of stations', 'D_indep' : 'dummy: at least one indepe'}


# Set the labels to index names
x_labels = df_reg_results.index

ax.errorbar(coefficients, x_labels, xerr=errors, linewidth=3, linestyle='None', marker='None', markeredgecolor='k', ecolor='r')	


# Set the labels and title
#ax.set_ylabel('Regression parameters')
ax.set_xlabel('Coefficient')
ax.set_title('DE: Regression results for fixed effects in clusters')


#ax.legend(loc='right')

ax.axis(xmin=-0.039,xmax=0.039)

plt.axvline(0, color='black')
plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

# Display the plot
#plt.show()

save_name = f'../plots/linreg/all-DE_linreg_cluster_FE_parameters.png'
fig.savefig(save_name, dpi = 150)
print('Saved: ' + save_name)


