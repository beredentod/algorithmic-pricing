from datetime import datetime, timedelta

import functions_1 as fcs
from functions_1 import df_linreg_prices


cluster = 'group90'

print(df_linreg_prices)

#fcs.calculateCycles(cluster, 18)







df_linreg_dummies = fcs.getDummies(df_linreg_prices, cluster)

print(df_linreg_dummies)



df_reg_results = fcs.getLinearRegression(df_linreg_dummies['price'], df_linreg_dummies.filter(like=cluster))
df_reg_results = fcs.addCharacteristics(df_reg_results)

#df_reg_results = df_reg_results.loc[df_reg_results['HHi'] < 1]

print(df_reg_results)

#df_reg_results.to_csv(cluster+'_characteristics.csv')





'''
import statsmodels.api as sm
Y = df_reg_results['Fixed effect'].astype(float)
X = df_reg_results[['HHi']].astype(float)
#import pdb; pdb.set_trace()

X = sm.add_constant(X)
model = sm.OLS(Y,X)
results = model.fit()

print(results.params)
'''
'''

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

#df_reg_results_HHi_n = fcs.getLinearRegression(df_reg_results['Fixed effect'], df_reg_results[['n', 'HHi']], True)
#df_reg_results_HHi_n = df_reg_results_HHi_n.drop('const')



#import pdb; pdb.set_trace()

df_reg_results_char = pd.concat([df_reg_results_HHi, df_reg_results_share, df_reg_results_Nindep, df_reg_results_Dindep, df_reg_results_n], axis=0)

print(df_reg_results_char)
'''

