from datetime import datetime
import pandas as pd

from load_char import df_char
from load_prices import df_prices


# select all stations' characteristics for a one brand on a particular date
def selectRowsbyBrand(date, brand):
	df_sel = df_char[df_char.apply(lambda row: row['first'] <= date <= row['last'], axis=1)]
	stations = df_sel[df_sel['brand_id'] == brand]
	return stations


# select a price row for a particular station on a particular date
def selectPriceRowsSingleStation(date, id_data):
	return df_prices.loc[(df_prices['id_data'] == id_data) & (df_prices['date'] == date)]


# select all the price rows for all the selected stations in df on a particular date
def selectPriceRows(date, df):
	return df_prices.loc[(df_prices['id_data'].isin(df['id_data'].values)) & (df_prices['date'] == date)]


# trim the dataframe to get just the time series of prices within a time interval
def trimToTimeSeries(df, start_time = '6:00', end_time = '22:55'):
	dt_start = datetime.strptime(start_time, '%H:%M').time()
	dt_end = datetime.strptime(end_time, '%H:%M').time()

	# the column indices for start and end 
	idx_start = None
	idx_end = None

	# find the next timestamp greater or equal to start_time
	for i, column in enumerate(df.columns):
		try:
			if column >= dt_start:
				idx_start = i
				break
		except TypeError:
			pass

	# find the previous timestamp smaller or equal to end_time
	for i, column in reversed(list(enumerate(df.columns))):
			try:
				if column <= dt_end:
					idx_end = i+1
					break
			except TypeError:
				pass

	# trim the dataframe
	return df.iloc[:, [0] + list(range(idx_start,idx_end))]
