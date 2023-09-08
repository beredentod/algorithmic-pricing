from datetime import datetime, timedelta
import numpy as np
import pandas as pd

import functions_1 as fcs


single_date = datetime(2022, 10, 3)
start_date = datetime(2022, 10, 1)
end_date = datetime(2022, 10, 31)
param = 'all'
arg = 'all'


df_stations = fcs.selectStationsbyCategory(single_date, param, arg)
df_prices = fcs.selectPriceRows(single_date, df_stations)

#print(df_prices)


(df_stations, df_prices) = fcs.selectStationsbyCategoryRange(start_date, end_date, param, arg)

#print(df_stations)
print(df_prices)



# create a time series
#df_prices_ts = fcs.trimToTimeSeries(df_prices)


cluster = 'group90'

# create errors bars
df_prices_eb = fcs.createTableForLinReg(df_prices)
df_prices_eb = fcs.getDummies(df_stations, df_prices_eb, cluster)

print(df_prices_eb)



df_reg_results = fcs.getLinearRegression(df_prices_eb['price'], df_prices_eb.filter(like=cluster))
df_reg_results = fcs.addCharacteristics(df_stations, df_reg_results)

print(df_reg_results)

#df_reg_results_char = fcs.getLinearRegression()






