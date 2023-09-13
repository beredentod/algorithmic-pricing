from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import functions_1 as fcs


single_date = datetime(2022, 10, 3)
param = 'all'
arg = 'all'

# for single date, filter by a parameter

#df_stations = fcs.selectStationsbyCategory(single_date, param, arg)
#df_prices = fcs.selectPriceRowsDate(single_date, df_stations)
#print(df_prices)


start_date = datetime(2022, 10, 1)
end_date = datetime(2022, 10, 31)

df_prices = fcs.selectPriceAllRowsRange(start_date, end_date)


#print(df_stations)
#print(df_prices)



# create a time series
#df_prices_ts = fcs.trimToTimeSeries(df_prices)


cluster = 'group90'

# create errors bars
df_prices_eb = fcs.createTableForLinReg(df_prices)
df_prices_eb = fcs.getDummies(df_prices_eb, cluster)

print(df_prices_eb)



df_reg_results = fcs.getLinearRegression(df_prices_eb['price'], df_prices_eb.filter(like=cluster))
df_reg_results = fcs.addCharacteristics(df_reg_results)

#df_reg_results = df_reg_results.loc[df_reg_results['HHi'] < 1]

print(df_reg_results)

import statsmodels.api as sm


'''
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

