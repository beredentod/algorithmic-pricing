from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import statsmodels.api as sm

from load_char_0a import df_char
from load_prices_0b import df_prices


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
def selectPriceRowsDate(date, df_stations_filtered):
	df_sel_prices = df_prices.loc[(df_prices['id_data'].isin(df_stations_filtered['id_data'].values)) & (df_prices['date'] == date)]
	df_sel_prices = df_sel_prices.dropna()
	return df_sel_prices


# select all price rows within a date range
def selectPriceAllRowsRange(start_date, end_date):
	df_sel_prices = df_prices[(df_prices['date'] >= start_date) & (df_prices['date'] <= end_date)]
	df_sel_prices = df_sel_prices.dropna()
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

	df.set_index('id_data', inplace=True)

	# trim the dataframe
	return df.iloc[:, idx_start-1:idx_end]


###
#
# Visuals / Utils
#
###


# look up an address of a station based on its id_data
def lookUpAddress(id_data, show_brand_id = False):
	street = df_char.loc[df_char[df_char['id_data'] == id_data].index[0]].at['street']
	house_number = df_char.loc[df_char[df_char['id_data'] == id_data].index[0]].at['house_number']
	brand_id = df_char.loc[df_char[df_char['id_data'] == id_data].index[0]].at['brand_id']

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
	melted_df = pd.melt(new_df, id_vars=['id_data', 'date'], var_name='hour', value_name='price')

	# combine columns 'date' and 'hour' into one column 'timestamp'
	melted_df['timestamp'] = melted_df.apply(lambda row: datetime.combine(row['date'], row['hour']), axis=1)

	# drop the unnecessary columns
	melted_df = melted_df[['id_data', 'timestamp', 'price']]

	# sort first by id_data, then by 'timestamp'
	melted_df = melted_df.sort_values(by=['id_data', 'timestamp'])

	# reset index after sorting
	melted_df.reset_index(drop=True, inplace=True)

	return melted_df


# get dummies for linear regression according to the needed category
def getDummies(df_prices_filtered, category = 'group85'):
	merged_df = pd.merge(df_prices_filtered, df_char[['id_data', category]], on='id_data', how='left')

	# Convert 'groupXX' column to dummies
	dummies = pd.get_dummies(merged_df[category], prefix=category)

	# Concatenate the dummies with the original DataFrame
	concat_df = pd.concat([merged_df, dummies], axis=1)

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



## TODO
# Discuss with ML if it can be done quicker

def addCharacteristics(df_reg_results):

	# 1) number of stations in cluster
	df_reg_results['n'] = np.nan

	# 2) is at least one station independent (not corporate brand)?
	df_reg_results['D_indep'] = np.nan

	# 3) number of independent stations in cluster
	df_reg_results['n_indep'] = np.nan

	# 4) share of independent stations in cluster
	df_reg_results['share_indep'] = np.nan

	# 5) Herfindahl-Hirschman index for market concentration
	df_reg_results['HHi'] = np.nan


	df_reg_results = df_reg_results.rename(columns={'Coefficient': 'Fixed effect', 'Lower CI': 'FE lower CI', 'Upper CI': 'FE upper CI'})

	for idx, row in df_reg_results.iterrows():
		(cluster, number) = idx.split('_')

		# get the dataframe just for the iterated cluster
		df_cluster = getStationsInCluster(cluster, int(number))

		# get the number of stations in cluster
		count = len(df_cluster)
		df_reg_results.at[idx, 'n'] = count

		# get independent stations in cluster
		df_indep = removeCorporations(df_cluster)

		# get the number of independent stations
		count_indep = len(df_indep)
		df_reg_results.at[idx, 'n_indep'] = count_indep

		# get the share of independent stations
		df_reg_results.at[idx, 'D_indep'] = (count_indep > 0)

		# get the share of independent stations
		share_indep = count_indep/count
		df_reg_results.at[idx, 'share_indep'] = share_indep

		# get Herfindahl-Hirschman index for cluster
		df_reg_results.at[idx, 'HHi'] = calculateMarketConcentration(df_cluster)
	

	return df_reg_results
