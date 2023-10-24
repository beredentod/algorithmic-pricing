from datetime import datetime, timedelta

import pandas as pd

import functions_1 as fcs


single_date = datetime(2022, 10, 5)
param = 'group80'
arg = 1

# for single date, filter by a parameter

df_stations = fcs.selectStationsbyCategory(single_date, param, arg)
df_prices = fcs.selectPriceRowsDate(single_date, df_stations, True)
#print(df_prices)

date = single_date

#print(df_stations)
print(df_prices)

# create a time series
df_prices_ts = fcs.trimToTimeSeries(df_prices)


#df_prices_mean = pd.DataFrame({'mean_price': df_prices.iloc[:, 4:].mean()})
#df_prices_mean['price_delta'] = df_prices_mean['mean_price'] - df_prices_mean['mean_price'].shift(1) + 0.00001
#df_prices_mean['price_delta2'] = df_prices_mean['price_delta'] - df_prices_mean['price_delta'].shift(1)
#df_prices_mean['mult'] = df_prices_mean['price_delta'] * df_prices_mean['price_delta2']

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#	print(df_prices_mean)


'''
df_prices_linreg = fcs.createTableForLinReg(df_prices)



df_prices_linreg['price_delta'] = df_prices_linreg['price'] - df_prices_linreg['price'].shift(1) + 0.00001
df_prices_linreg['price_delta2'] = df_prices_linreg['price_delta'] - df_prices_linreg['price_delta'].shift(1)
df_prices_linreg['mult'] = df_prices_linreg['price_delta'] * df_prices_linreg['price_delta2']


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(df_prices_linreg[['timestamp', 'price', 'price_delta', 'price_delta2', 'mult']])

count_cycles = (df_prices_mean['mult'].dropna() < 0).sum()

#print(count_cycles)



# create a time series
df_prices_ts = fcs.trimToTimeSeries(df_prices)


import numpy as np
from scipy.signal import find_peaks



time_series = np.array(df_prices.iloc[:, 4:].mean())

# Peak detection parameters
height = 1.94  # Adjust as needed
distance = 10  # Adjust as needed
threshold = None  # Adjust as needed

peaks, _ = find_peaks(time_series, height=height, distance=distance, threshold=threshold)

print(len(peaks))


import matplotlib.pyplot as plt
# Plot the time series
plt.plot(time_series, label='Time Series')

# Mark the significant peaks
plt.plot(peaks, time_series[peaks], 'ro', label='Significant Peaks')

plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series with Significant Local Maxima')
plt.show()
'''