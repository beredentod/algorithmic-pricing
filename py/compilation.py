from datetime import datetime, timedelta

import functions as fcs


date = datetime(2022, 10, 6)
param = 'all'
arg = 4


df_stations = fcs.selectStationsbyCategory(date, param, arg)
df_prices = fcs.selectPriceRows(date, df_stations)


# create a time series
#df_prices_ts = fcs.trimToTimeSeries(df_prices)


cluster = 'group80'

# create errors bars
df_prices_eb = fcs.createTableForLinReg(df_prices)
df_prices_eb = fcs.getDummies(df_stations, df_prices_eb, cluster)

print(df_prices_eb)

df_reg_results = fcs.runLinearRegression(df_prices_eb, cluster)
df_reg_results = fcs.addCharacteristics(df_stations, df_reg_results)

print(df_reg_results)







