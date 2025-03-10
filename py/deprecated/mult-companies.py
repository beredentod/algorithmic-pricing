import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd

import stations_colors as sc


MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')



'''
Yields a times series of prices in Munich for multiple brands for one particular day 

'''



# returns the list of all individual stations within the brand (returns 'id_data' of each station)
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


# create labels for the graph for each station as "street & no. "
def createGraphLabelsForStations(ids):
	names = []

	for x in ids:
		street = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['street']
		house_number = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['house_number']
		names.append(str(street) + " " + str(house_number))

	return names


def updateOverallAverage(avg_range, count, brand_avg_range, size):
	for idx, val in enumerate(brand_avg_range):
		avg_range[idx] *= count
		avg_range[idx] += val*size
		avg_range[idx] /= (count+size)
	count += size
	return (avg_range, count)


string = input("Date: ")
date = string+'oct2022'
#company = input("Company: ")


companies = ['aral', 'shell', 'agip', 'esso', 'jet', 'omv', 'allguth']

#date = '03oct2022'



avgs = []
names = []

AVG = [0] * 204 
count = 0


for i in companies:
	(ranges, ids) = getDataAllStationsOneBrand(i, date)
	if ranges != []:
		temp_avg = calculateAveragesOneBrand(ranges)
		(AVG, count) = updateOverallAverage(AVG, count, temp_avg, len(ranges))
		avgs.append(temp_avg)
		names.append(i)


avgs.append(AVG)
names.append('AVERAGE across all stations')


times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
rangeX = times

#import pdb; pdb.set_trace()

fig, ax = plt.subplots()


for idx, rr in enumerate(avgs[:-1]):
	ax.plot_date(rangeX, rr, label=names[idx], fmt='')	
	

ax.plot_date(rangeX, avgs[-1], label=names[-1], fmt='', zorder = 100, linewidth=3, color='black')


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
ax.set_ylim(low, high)


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title('Munich: AVG prices across brands on '+date)
ax.legend(loc="lower center", ncol=5)


# maximize the preview window 
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

plt.show()


# saving the plot
plt.rcParams["figure.figsize"] = [14, 8] # the size of the figure to be saved
save_name = './samples/avg_stations_MUC_'+date+'.png'
plt.gcf().set_size_inches(14, 8)
fig.savefig(save_name, dpi = 300, format='png', orientation='landscape')
print('Saved: ' + save_name)

