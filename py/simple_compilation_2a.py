from datetime import datetime, timedelta

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

df_prices = fcs.selectPriceAllRowsRange(start_date, end_date, True)


#print(df_stations)
print(df_prices)



# create a time series
#df_prices_ts = fcs.trimToTimeSeries(df_prices)
