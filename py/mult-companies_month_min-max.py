import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import math
import pandas as pd

import stations_colors as sc


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


def updateOverallAverage(avg_range, count, brand_avg_range, size):
	for idx, val in enumerate(brand_avg_range):
		avg_range[idx] *= count
		avg_range[idx] += val*size
		avg_range[idx] /= (count+size)
	count += size
	return (avg_range, count)





#string = input("Date: ")
#date = string+'oct2022'
#company = input("Company: ")
company = 'aral'

companies = ['aral', 'shell', 'agip', 'esso']

dates =  ['0'+str(x)+'oct2022' for x in range(1, 10)]
dates = dates + [str(x)+'oct2022' for x in range(10, 32)]


mins = []
maxs = []
avgs = []
varis = [] # variance


for c in companies:
	temp_mins = []
	temp_maxs = []
	temp_avgs = []
	temp_varis = []

	for i in dates:
		(ranges, ids) = getDataAllStationsOneBrand(c, i)
		minv = 10000
		maxv = -1
		avg = 0
		count = 0
		if ranges != []:
			for j in ranges:
				for k in j:
					maxv = max(maxv, k)
					minv = min(minv, k)
					avg += k
					count += 1 

			avg /= count
			temp_mins.append(minv)
			temp_maxs.append(maxv)
			temp_avgs.append(avg)

			t_sum = 0
			for j in ranges:
				for k in j:
					t_sum += (k - avg)*(k - avg)
			S = t_sum/count
			temp_varis.append(S)		

	mins.append(temp_mins)
	maxs.append(temp_maxs)
	avgs.append(temp_avgs)
	varis.append(temp_varis)


mean_upper = []
mean_lower = []

for idx, c in enumerate(companies):
	temp_upper = []
	temp_lower = []
	for jdx, val in enumerate(avgs[idx]):
		temp_upper.append(avgs[idx][jdx] + varis[idx][jdx])
		temp_lower.append(avgs[idx][jdx] - varis[idx][jdx])
	mean_upper.append(temp_upper)
	mean_lower.append(temp_lower)



days = (pd.date_range(start='2022-10-01', end='2022-10-31', freq="1d")).to_numpy()
rangeX = days

fig, ax = plt.subplots()


for idx, val in enumerate(companies):
	ax.plot_date(rangeX, mean_upper[idx], label="MEAN+VAR " + val, marker='', linestyle='-.', linewidth=0.5, color=sc.hex_to_rgb(sc.colors_brands[val]))	
	ax.plot_date(rangeX, mean_lower[idx], label="MEAN-VAR " + val, marker='', linestyle='-.', linewidth=0.5, color=sc.hex_to_rgb(sc.colors_brands[val]))
	ax.plot_date(rangeX, mins[idx], label="MIN " + val, marker='', linestyle='--', color=sc.hex_to_rgb(sc.colors_brands[val]))	
	ax.plot_date(rangeX, maxs[idx], label="MAX " + val, marker='', linestyle='--', color=sc.hex_to_rgb(sc.colors_brands[val]))	
	ax.plot_date(rangeX, avgs[idx], label="MEAN " + val, marker='', linestyle='-', linewidth=2, color=sc.hex_to_rgb(sc.colors_brands[val]))	
	

#ax.plot_date(rangeX, avgs[-1], label=names[-1], marker='', linestyle='-', zorder = 100, linewidth=3, color='black')


# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%d')
ax.xaxis.set_major_formatter(myFmt)



# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
ax.set_ylim(low, high)
ax.set_xlim([dt.date(2022, 10, 1), dt.date(2022, 10, 31)])


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_xlabel('Days in October 2022')
ax.set_title('Munich: MIN and MAX prices on each day in October 2022')
ax.legend(loc="lower center", ncol=4)


# maximize the preview window 
manager = plt.get_current_fig_manager()
manager.window.showMaximized()

plt.show()


# saving the plot
plt.rcParams["figure.figsize"] = [14, 8] # the size of the figure to be saved
save_name = './samples/MIN_MAX_october2022_MUC_.png'
plt.gcf().set_size_inches(14, 8)
fig.savefig(save_name, dpi = 300, format='png', orientation='landscape')
print('Saved: ' + save_name)

