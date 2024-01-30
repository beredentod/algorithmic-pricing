from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
#from functions_1 import df_linreg_prices
from functions_1 import df_daily_station_linreg


cluster = 'group85'


df_cluster_char = fcs.getClusterCharacteristics(cluster)

#df_cluster_char['group85'] = 'group85_' + df_cluster_char['group85'].astype(str)

# Set the modified "group" column as the index
#df_cluster_char.set_index('group85', inplace=True)

print(df_cluster_char)


#filename = cluster_type+'_all_characteristics.csv'
#df_cluster_char.to_csv(filename, index=False)
#print('Saved! ' + filename)



#print(df_linreg_prices)

#fcs.calculateCycles(cluster, 18)

'''
df_linreg_dummies = fcs.getDummies(df_linreg_prices, cluster)

#print(df_linreg_dummies)


df_reg_results = fcs.getLinearRegression(df_linreg_dummies['price'], df_linreg_dummies.filter(like=cluster))
df_reg_results = fcs.addCharacteristics(df_reg_results)

df_reg_results = df_reg_results.drop(columns = ['FE lower CI', 'FE upper CI'])

df_reg_results['n'] = df_reg_results['n'].astype(int)
df_reg_results['n_indep'] = df_reg_results['n_indep'].astype(int)



print(df_reg_results)'''


#df_reg_results.to_csv(cluster+'_all_characteristics.csv')


df_reg_results = df_cluster_char

#df_reg_results = df_reg_results.loc[df_reg_results['HHi'] < 1] # no monopolist clusters

nan_rows = df_reg_results[df_reg_results['Fixed effect'].isna()]
print(nan_rows)

df_reg_results = df_reg_results.dropna()



import statsmodels.api as sm
Y = df_reg_results['Fixed effect'].astype(float)
X = df_reg_results[['HHi']].astype(float)
#import pdb; pdb.set_trace()

X = sm.add_constant(X)
model = sm.OLS(Y,X)
results = model.fit()

print(results.params)


df_reg_results_HHi = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['HHi']], True)
df_reg_results_HHi = df_reg_results_HHi.drop('const')

df_reg_results_share = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['share_indep']], True)
df_reg_results_share = df_reg_results_share.drop('const')

df_reg_results_Nindep = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['n_indep']], True)
df_reg_results_Nindep = df_reg_results_Nindep.drop('const')

df_reg_results_Dindep = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['D_indep']], True)
df_reg_results_Dindep = df_reg_results_Dindep.drop('const')

df_reg_results_n = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['n']], True)
df_reg_results_n = df_reg_results_n.drop('const')

df_reg_results_HHi_n = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['n', 'HHi']], True)
df_reg_results_HHi_n = df_reg_results_HHi_n.drop('const')



#import pdb; pdb.set_trace()

df_reg_results_char = pd.concat([df_reg_results_HHi, df_reg_results_share, df_reg_results_Nindep, df_reg_results_Dindep, df_reg_results_n], axis=0)

print(df_reg_results_char)


