from datetime import datetime
import pandas as pd
import statsmodels.api as sm

from load_char import df_char
from load_prices import df_prices



# select all stations' characteristics for one parameter on a particular date
# date - datetime
# par - string, e.g. 'brand_id'
# arg - (respective type)
def selectStationsbyCategory(date, par, arg):
	df_sel = df_char[df_char.apply(lambda row: row['first'] <= date <= row['last'], axis=1)]

	if par == 'all':
		return df_sel

	stations = df_sel[df_sel[par] == arg]
	return stations


####
# TODO #
# write a method that chooses whole month of data
####


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
					idx_end = i
					break
			except TypeError:
				pass

	df.set_index('id_data', inplace=True)

	# trim the dataframe
	return df.iloc[:, idx_start-1:idx_end]



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



# create a dataframe table in which every column with hour timestamp is replaced by a row with the timestamp with the respective price
def createTableForLinReg(df_prices):
	# drop redundant columns
	new_df = df_prices.drop(columns=['dow', 'weekend']) 

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



# get dummies for linear regression
def getDummies(df_stations, df_prices, category = 'group85'):
	merged_df = pd.merge(df_prices, df_stations[['id_data', category]], on='id_data', how='left')

	# Convert 'groupXX' column to dummies
	dummies = pd.get_dummies(merged_df[category], prefix=category)

	# Concatenate the dummies with the original DataFrame
	concat_df = pd.concat([merged_df, dummies], axis=1)

	# Drop the original category column if needed
	concat_df.drop(columns=[category], inplace=True)

	return(concat_df) 



def runLinearRegression(df_prices, category = 'group85'):
	Y = df_prices['price']
	X = df_prices.filter(like=category)

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



def getStationsInCluster(df_stations, cluster_name, arg):
	return (df_stations[df_stations[cluster_name] == arg])


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


def addCharacteristics(df_stations, df_reg_results):

	# 1) number of stations in cluster
	df_reg_results['n'] = pd.Series([], dtype=object) 

	# 2) is at least one station independent (not corporate brand)?
	df_reg_results['D^indep>1'] = pd.Series([], dtype=object) 

	# 3) number of independent stations in cluster
	df_reg_results['n^indep'] = pd.Series([], dtype=object)

	# 4) share of independent stations in cluster
	df_reg_results['share^indep'] = pd.Series([], dtype=object)

	# 5) Herfindahl-Hirschman index for market concentration
	df_reg_results['HHi'] = pd.Series([], dtype=object)


	for idx, row in df_reg_results.iterrows():
		index_parts = idx.split('_')

		# get the dataframe just for the iterated cluster
		df_cluster = getStationsInCluster(df_stations, index_parts[0], int(index_parts[1]))

		# get the number of stations in cluster
		count = len(df_cluster)
		df_reg_results.at[idx, 'n'] = count

		# get independent stations in cluster
		df_indep = removeCorporations(df_cluster)

		# get the number of independent stations
		count_indep = len(df_indep)
		df_reg_results.at[idx, 'n^indep'] = count_indep

		# get the share of independent stations
		df_reg_results.at[idx, 'D^indep>1'] = (count_indep > 0)

		# get the share of independent stations
		share_indep = count_indep/count
		df_reg_results.at[idx, 'share^indep'] = share_indep

		# get Herfindahl-Hirschman index for cluster
		df_reg_results.at[idx, 'HHi'] = calculateMarketConcentration(df_cluster)
	

	return df_reg_results