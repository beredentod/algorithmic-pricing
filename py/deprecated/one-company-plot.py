'''
File: one-company-plot.py
- yields a times series of prices in Munich for all stations
	of one particular brand on one date, range: 6:00 until 22:55
'''


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd


MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


# returns the list of all stations within the brand (returns 'id_data' of each station)
def getStationsbyCompany(comp_name):
	stations = MUC_char[MUC_char['brand_id'] == comp_name]
	ids = stations['id_data'].tolist()
	return ids


# get time series of prices for one particular station (based on 'id_data') on a particular date
def getDataSingleStation(local_id_data, local_date):
	temp = MUC_data.loc[(MUC_data['id_data'] == local_id_data) & (MUC_data['date'] == local_date)]

	# if the data set includes the given station for the given date
	if not temp.empty:
		temp = temp.iloc[:, 4:]  # takes the data from 4th column onwards ('6:00', '6:05', ...)
		r = (temp.to_numpy())[0] # returns a nested array ('[[val]]'), so we need [0] to unnest the array
		return r

	# returns None if there is no data for the given station on the given date
	return 


# get times series for all stations within a company on a particular date
def getDataAllStationsOneBrand(local_company, local_date):
	ids =[] # 'id_data' of each station
	ranges = []	

	# list of 'id_data' for $company
	stations = getStationsbyCompany(local_company)

	for s in stations:
		ret = getDataSingleStation(s, local_date)

		# skip if there is no data for a particular station on a particular date
		if ret is not None: 
			ranges.append(ret)
			ids.append(s)

	# ([times series], ['id_data' for each station])
	return (ranges, ids)


# get a time series containing the average price across all stations of one brand for each time recording
def calculateAveragesOneBrand(ranges):
	avg = []

	for idx, val in enumerate(ranges[0]): # idx is the iterator over index of each price in time recording
		temp_sum = 0
		for rr in ranges: # sum the prices at index idx for each station
			temp_sum += rr[idx]
		temp_sum /= len(ranges) # divide by the number of stations
		avg.append(temp_sum)

	return avg


# create labels the graph for each station as "street & no. "
def createGraphLabelsForStations(ids):
	names = []

	for x in ids:
		street = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['street']
		house_number = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['house_number']
		names.append(str(street) + " " + str(house_number))

	return names




# input the date for which the 
# format: two-digit number
# range: 01 - 31 October 2022
string = input("Date: ")
date = string+'oct2022'

# input the brand of the stations
company = input("Company: ")


# get all time series for each station within the brand
# ranges - array with a time series for each station
# ids - array with the ids of each station
(ranges, ids) = getDataAllStationsOneBrand(company, date)


# calculate average for each time stamp (5-min interval)
avg_company = calculateAveragesOneBrand(ranges)


# create labels each station on the graph, format: "street" + "no." 
# names - the array with the labels for the graph
names = createGraphLabelsForStations(ids)


# add the average time series to the array of all time series
ranges.append(avg_company)
names.append("AVERAGE") # add the label to the array with all labels


# create the time series range for the graph: from 6:00 until 22:55 with 5-min intervals
times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
rangeX = times


# create figure with fixed size (16, 9)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1) # just one graph (one subplot)


# add each time series to the graph
for idx, rr in enumerate(ranges):
	ax.plot_date(rangeX, rr, fmt='-', label=names[idx])


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215 # max based on the data given
ax.set_ylim(low, high)


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title('Munich: '+company.title()+' stations on Oct '+string+' 2022')
ax.legend(loc="lower center", ncol=5)


# maximize the preview window 
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

plt.show()


# saving the plot
fig.savefig('./samples/'+company+'_stations_MUC_'+date+'.png', dpi = 400)
print('Saved: ' + './samples/'+company+'_stations_MUC_'+date+'.png')

