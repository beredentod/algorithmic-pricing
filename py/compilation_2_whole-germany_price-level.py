from datetime import datetime, timedelta
import pandas as pd

import functions_1 as fcs
from functions_1 import df_daily_station_linreg


dic = {}

big_oil = ['aral', 'shell', 'esso', 'total', 'jet']
smaller_integrated = ['agip', 'hem', 'omv', 'star', 'avia', 'bft']


for brand in big_oil:

	df = df_daily_station_linreg[df_daily_station_linreg['brand_id'] == brand]
	grouped = df.groupby('date')['price_mean'].mean()

	dic[brand] = grouped


df_integ = df_daily_station_linreg[df_daily_station_linreg['brand_id'].isin(smaller_integrated)]
grouped = df.groupby('date')['price_mean'].mean()
dic['other_integrated'] = grouped


df_other = df_daily_station_linreg[~df_daily_station_linreg['brand_id'].isin((smaller_integrated + big_oil))]
grouped = df.groupby('date')['price_mean'].mean()
dic['non-integrated'] = grouped


print(df_other)
