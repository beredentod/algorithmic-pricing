from datetime import datetime

import functions as fcs


date = datetime(2022, 10, 1)
brand = 'agip'


df_stations = fcs.selectRowsbyBrand(date, brand)
df_prices = fcs.selectPriceRows(date, df_stations)
df_prices = fcs.trimToTimeSeries(df_prices)


print(df_prices.iloc[:, 1:].values)

print(df_prices.iloc[0, 0])
