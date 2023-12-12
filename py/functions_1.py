from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks

from load_char_0a import df_char
from load_prices_0b import df_prices
from load_linreg_prices_0c import df_linreg_prices
from load_price_inc_0d import df_price_inc
from load_daily_station_linreg_0e import df_daily_station_linreg



###
#
# Reading & compiling data
#
###


# select all stations' characteristics for one parameter on a particular date
# date - datetime
# param - string, e.g. 'brand_id'
# arg - string or number (respective type), argument for parameter
def selectStationsbyCategory(date, param, arg):

	# select all stations for which data is available on given date
	df_sel = df_char.loc[(df_char['first'] <= date) & (df_char['last'] >= date)]

	# if the parameter is 'all' return all stations at this points
	if param == 'all':
		return df_sel

	# if a parameter is entered, filter by the given parameter
	return df_sel[df_sel[param] == arg]


# select a price row for a particular station (id_data) on a particular date
def selectPriceRowsSingleStation(date, id_data):
	return df_prices.loc[(df_prices['id_data'] == id_data) & (df_prices['date'] == date)]


# select all price rows for all selected stations in df on a particular date
def selectPriceRowsDate(date, df_stations_filtered, id_data_updated = False):
	df_sel_prices = df_prices.loc[(df_prices['id_data'].isin(df_stations_filtered['id_data'].values)) & (df_prices['date'] == date)]
	df_sel_prices = df_sel_prices.dropna()

	if id_data_updated == True:
		return utilSwapIdDataColumns(df_sel_prices)

	return df_sel_prices


def utilSwapIdDataColumns(df):
	merged_df = df.merge(df_char[['first', 'last', 'id_data', 'id_data_updated']], on='id_data', how='left')
	merged_df = merged_df[(merged_df['date'] >= merged_df['first']) & (merged_df['date'] <= merged_df['last'])]

	merged_df.drop(columns=['id_data', 'first', 'last'], inplace=True)
	#merged_df.drop(columns=['first', 'last'], inplace=True)

	column_data = merged_df['id_data_updated']
	merged_df.drop(columns='id_data_updated', inplace=True)
	merged_df.insert(0, 'id_data_updated', column_data)

	#merged_df = merged_df.merge(df_char[['id_data_updated', 'group80', 'group85', 'group90']], on='id_data_updated', how='left')

	#pd.set_option('display.max_rows', None)

	#print(merged_df.loc[merged_df['id_data_updated'] == '2aa5a805-38a3-450c-b92b-f08c78a5fad4-1'])
	#print(merged_df)

	#import pdb; pdb.set_trace()

	#pd.reset_option('display.max_rows')

	return merged_df


# select all price rows within a date range
def selectPriceAllRowsRange(start_date, end_date, id_data_updated = False):
	df_sel_prices = df_prices[(df_prices['date'] >= start_date) & (df_prices['date'] <= end_date)]
	df_sel_prices = df_sel_prices.dropna()

	if id_data_updated == True:
		return utilSwapIdDataColumns(df_sel_prices)

	return df_sel_prices



# select all price rows for all selected stations in df within a date range
def selectStationsbyCategoryRange(start_date, end_date, param, arg):

	#TODO
	#problably could be done quicker:
	#1)take all price rows
	#2)filter price rows by dates
	#3)remove price rows that are not relevant

	#TODO
	#assert(start_date <= end_date, "Start date is greater than end date.")

	current_date = start_date

	df_stations = selectStationsbyCategory(current_date, param, arg)
	df_prices_filtered = selectPriceRowsDate(current_date, df_stations)

	# iterate over dates until end_date achieved
	while current_date < end_date:
		current_date += timedelta(days=1)  # Increment the date by 1 day
	    
		df_stations_temp = selectStationsbyCategory(current_date, param, arg)
		df_prices_temp = selectPriceRowsDate(current_date, df_stations)	

		# for each date concat all stations and remove duplicates 
		#TODO
		#probably could be done quicker (a lot of redundant steps)
		df_stations = pd.concat([df_stations, df_stations_temp], ignore_index=True)
		df_stations = df_stations.drop_duplicates(subset=['id_data'])

		# for each date concat all price rows on top of each other
		df_prices_filtered = pd.concat([df_prices_filtered, df_prices_temp], ignore_index=True)
	

	# return filtered stations & the concat'ed price rows
	return (df_stations, df_prices_filtered)    



# trim the dataframe to get just the time series of prices within a time interval
# input: dataframe with price rows and columns 6:00, 6:05, ...
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
					idx_end = i
					break
			except TypeError:
				pass

	df.set_index('id_data_updated', inplace=True)

	# trim the dataframe
	return df.iloc[:, idx_start-1:idx_end]


###
#
# Visuals / Utils
#
###


# look up an address of a station based on its id_data
def lookUpAddress(id_data, show_brand_id = False):

	id_data_type = 'id_data_updated'

	street = df_char.loc[df_char[df_char[id_data_type] == id_data].index[0]].at['street']
	house_number = df_char.loc[df_char[df_char[id_data_type] == id_data].index[0]].at['house_number']
	brand_id = df_char.loc[df_char[df_char[id_data_type] == id_data].index[0]].at['brand_id']

	if show_brand_id == False:
		# combine street and number into an address
		return str(street) + ' ' + str(house_number)
	else:
		# combine street and number into an address + add the brand
		return str(street) + ' ' + str(house_number) + ' [' + brand_id +']'


###
#
# Data processing
#
###


# create a dataframe table in which every column with hour timestamp is replaced 
# by a row with the timestamp with the respective price
def createTableForLinReg(df_prices_filtered):
	# drop redundant columns
	new_df = df_prices_filtered.drop(columns=['dow', 'weekend']) 

	# make a separate row with price out of each hour timestamp 
	melted_df = pd.melt(new_df, id_vars=['id_data_updated', 'date'], var_name='hour', value_name='price')

	# combine columns 'date' and 'hour' into one column 'timestamp'
	melted_df['timestamp'] = melted_df.apply(lambda row: datetime.combine(row['date'], row['hour']), axis=1)

	# drop the unnecessary columns
	melted_df = melted_df[['id_data_updated', 'timestamp', 'price']]

	# sort first by id_data, then by 'timestamp'
	melted_df = melted_df.sort_values(by=['id_data_updated', 'timestamp'])

	# reset index after sorting
	melted_df.reset_index(drop=True, inplace=True)

	# add clusters for each price row
	melted_df = melted_df.merge(df_char[['id_data_updated', 'group80', 'group85', 'group90']], on='id_data_updated', how='left')

	return melted_df


# get dummies for linear regression according to the needed category
def getDummies(df_linreg, category = 'group85'):
	#merged_df = pd.merge(df_prices_filtered, df_char[['id_data_updated', category]], on='id_data_updated', how='left')

	#print(merged_df)
	#print(merged_df.loc[(merged_df['timestamp'].dt.strftime('%H:%M') == '06:00') & (merged_df[category] == 2)])

	# Convert 'groupXX' column to dummies
	dummies = pd.get_dummies(df_linreg[category], prefix=category)

	# Concatenate the dummies with the original DataFrame
	concat_df = pd.concat([df_linreg, dummies], axis=1)

	# Drop the original category column if needed
	concat_df.drop(columns=[category], inplace=True)

	return(concat_df) 


# generate linear regression for given datasets
def getLinearRegression(Y, X, add_constant = False):

	X = X.astype(float)
	Y = Y.astype(float)

	if add_constant:
		X = sm.add_constant(X)
	model = sm.OLS(Y, X)
	results = model.fit()

	df_results = pd.DataFrame({
	'Coefficient': results.params,
	'Lower CI': results.conf_int().iloc[:, 0],
	'Upper CI': results.conf_int().iloc[:, 1]
	})

	# Set the coefficients and errors
	coefficients = df_results['Coefficient'] # the calculated coefficients 
	errors = [df_results['Coefficient'] - df_results['Lower CI'], df_results['Upper CI'] - df_results['Coefficient']]

	return df_results


def calculateVarianceInCluster(df_linreg, cluster_type, cluster_id):
	df = df_linreg[df_linreg[cluster_type] == cluster_id]

	groups = df.groupby('timestamp')

	group_means = groups['price'].transform('mean')

	diffs = ((df['price'] - group_means) / group_means) * ((df['price'] - group_means) / group_means)

	return (diffs.sum()) / len(groups)



def getStationsInCluster(cluster_name, arg):
	return (df_char[df_char[cluster_name] == arg])


def calculateMarketConcentration(df_cluster):

	# number of stations in cluster
	grouped = df_cluster.groupby('brand_id').count()['id_data']

	# share of each brand's stations in the cluster
	grouped = grouped/grouped.sum()

	# multiply each share by itself
	grouped = grouped*grouped

	# add to calculate Herfindahl-Hirschman index
	return grouped.sum()


# remove stations from cluster that are corporate brands, leave 'independent' stations only
def removeCorporations(df_cluster):
    brands_to_remove = ['aral', 'esso', 'shell', 'jet', 'total', 'agip', 'hem', 'star', 'omv']
    return df_cluster[~df_cluster['brand_id'].isin(brands_to_remove)]



# WRONG
# calculate the mean number of cycles per day for each cluster
def calculateCycles(cluster_type, cluster_id):
	df_linreg_prices['timestamp'] = pd.to_datetime(df_linreg_prices['timestamp'])
	df_linreg_prices['date'] = df_linreg_prices['timestamp'].dt.date

	df_cluster_prices = df_linreg_prices[df_linreg_prices[cluster_type] == cluster_id]

	grouped = df_cluster_prices.groupby("date")

	peaks_by_day = []

	import matplotlib.pyplot as plt

	for _, group in grouped:
		timestamp_means = group.groupby('timestamp')['price'].mean()


		# CORRECT THE PARAMETERS!!!

		# Peak detection parameters
		height = 1.7  # Adjust as needed
		distance = 10  # Adjust as needed
		threshold = None

		peaks, _ = find_peaks(np.array(timestamp_means), height=height, distance=distance, threshold=threshold)

		number_of_peaks = len(peaks)
		peaks_by_day.append(number_of_peaks)

		# Plot the time series
		plt.plot(np.array(timestamp_means), label='Time Series')

		# Mark the significant peaks
		plt.plot(peaks, np.array(timestamp_means)[peaks], 'ro', label='Significant Peaks')

		plt.legend()
		plt.xlabel('Time')
		plt.ylabel('Value')
		plt.title('Time Series with Significant Local Maxima')
		plt.show()

	return(sum(peaks_by_day)/len(peaks_by_day))


def addCharacteristics(df_cluster_char):

	# 1) number of stations in cluster
	df_cluster_char['n'] = np.nan

	# 2) is at least one station independent (not corporate brand)?
	df_cluster_char['D_indep'] = np.nan

	# 3) number of independent stations in cluster
	df_cluster_char['n_indep'] = np.nan

	# 4) share of independent stations in cluster
	df_cluster_char['share_indep'] = np.nan

	# 5) Herfindahl-Hirschman index for market concentration
	df_cluster_char['HHi'] = np.nan

	# 6) Variance 
	#df_cluster_char['var'] = np.nan

	# 7) mean no. of cycles per day 
	#df_cluster_char['mean_cycles'] = np.nan


	df_cluster_char = df_cluster_char.rename(columns={'Coefficient': 'Fixed effect', 'Lower CI': 'FE lower CI', 'Upper CI': 'FE upper CI'})

	for idx, row in df_cluster_char.iterrows():
		(cluster, number) = idx.split('_')

		# get the data frame with df_stations just for the iterated cluster
		df_cluster = getStationsInCluster(cluster, int(number))

		# get the number of stations in cluster
		count = len(df_cluster)
		df_cluster_char.at[idx, 'n'] = int(count)

		# get independent stations in cluster
		df_indep = removeCorporations(df_cluster)

		# get the number of independent stations
		count_indep = len(df_indep)
		df_cluster_char.at[idx, 'n_indep'] = count_indep

		# get the share of independent stations
		df_cluster_char.at[idx, 'D_indep'] = (count_indep > 0)

		# get the share of independent stations
		share_indep = count_indep/count
		df_cluster_char.at[idx, 'share_indep'] = share_indep

		# get Herfindahl-Hirschman index for cluster
		df_cluster_char.at[idx, 'HHi'] = calculateMarketConcentration(df_cluster)

		# get variance
		#df_cluster_char.at[idx, 'var'] = calculateVarianceInCluster(df_linreg_prices, cluster, int(number))


		#df_cluster_char['n'] = df_cluster_char['n'].astype(int)
		#df_cluster_char['n_indep'] = df_cluster_char['n_indep'].astype(int)

	return df_cluster_char



def getClusterCharacteristics(cluster_type):
	cluster_size = df_char[cluster_type].value_counts().sort_index()

	# 1) number of stations in cluster
	df_cluster_char = pd.DataFrame({'n': cluster_size})

	# 2) is at least one station independent (not corporate brand)?
	df_cluster_char['D_indep'] = np.nan

	# 3) number of independent stations in cluster
	df_cluster_char['n_indep'] = np.nan

	# 4) share of independent stations in cluster
	df_cluster_char['share_indep'] = np.nan

	# 5) Herfindahl-Hirschman index for market concentration
	df_cluster_char['HHi'] = np.nan


	for idx, row in df_cluster_char.iterrows():

		# get the data frame with df_stations just for the iterated cluster
		df_cluster = getStationsInCluster(cluster_type, idx)

		# get the number of stations in cluster
		count = df_cluster_char.at[idx, 'n']

		# get independent stations in cluster
		df_indep = removeCorporations(df_cluster)

		# get the number of independent stations
		count_indep = len(df_indep)
		df_cluster_char.at[idx, 'n_indep'] = count_indep

		# get the share of independent stations
		df_cluster_char.at[idx, 'D_indep'] = (count_indep > 0)

		# get the share of independent stations
		share_indep = count_indep/count
		df_cluster_char.at[idx, 'share_indep'] = share_indep

		# get Herfindahl-Hirschman index for cluster
		df_cluster_char.at[idx, 'HHi'] = calculateMarketConcentration(df_cluster)


	# Renaming the index to match the format 'group85_1', 'group85_2', 'group85_3', ...
	#df_cluster_char.index = ['group85_' + str(i) for i in df_cluster_char.index]
	df_cluster_char = df_cluster_char.reset_index().rename(columns={'index': cluster_type})

	df_cluster_char['n_indep'] = df_cluster_char['n_indep'].astype(int)

	return df_cluster_char