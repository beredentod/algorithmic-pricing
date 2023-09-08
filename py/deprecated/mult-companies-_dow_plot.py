import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
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



#string = input("Date: ")
#date = string+'oct2022'
company = input("Company: ")


companies = ['aral', 'shell', 'agip', 'esso', 'jet', 'omv', 'allguth', 'total', 'avia','bavarian petrol', 'sprint', 'v-markt', 'hem']

dates = ['03oct2022', '10oct2022', '17oct2022', '24oct2022', '31oct2022']


weekdays = [
['03oct2022', '10oct2022', '17oct2022', '24oct2022'],
['04oct2022', '11oct2022', '18oct2022', '25oct2022'],
['05oct2022', '12oct2022', '19oct2022', '26oct2022'],
['06oct2022', '13oct2022', '20oct2022', '27oct2022'],
['07oct2022', '14oct2022', '21oct2022', '28oct2022'],
['01oct2022', '08oct2022', '15oct2022', '22oct2022'],
['02oct2022', '09oct2022', '16oct2022', '23oct2022']]


avgs = []
names = ['week1 (Oct 1-7)', 'week2 (Oct 8-14)', 'week3 (Oct 15-21)', 'week4 (Oct 22-28)']


for d in weekdays:
	temp_avg = []
	for i in d:
		(ranges, ids) = getDataAllStationsOneBrand(company, i)
		if ranges != []:
			avg_company = calculateAveragesOneBrand(ranges)
			temp_avg.append(avg_company)
	avgs.append(temp_avg)



times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
rangeX = times


fig, axs = plt.subplots(nrows=7, ncols=1, figsize=(8, 20))

for i, ax in enumerate(fig.axes):
	for idx, rr in enumerate(avgs[i]):
		ax.plot_date(rangeX, rr, label=names[idx], marker='', linestyle='-')	


#color=sc.hex_to_rgb(sc.colors_brands[companies[idx]])



# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
for ax in fig.axes:
	ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
for ax in fig.axes:
	ax.set_ylim(low, high)
	#ax.axes.get_xaxis().set_visible(False)

#axs[6].axes.get_xaxis().set_visible(True)


axs[0].set_title('Mon', loc='right', y=1.0, pad=-14)
axs[1].set_title('Tue', loc='right', y=1.0, pad=-14)
axs[2].set_title('Wed', loc='right', y=1.0, pad=-14)
axs[3].set_title('Thu', loc='right', y=1.0, pad=-14)
axs[4].set_title('Fri', loc='right', y=1.0, pad=-14)
axs[5].set_title('Sat', loc='right', y=1.0, pad=-14)
axs[6].set_title('Sun', loc='right', y=1.0, pad=-14)


fig.supylabel('Price in Euro')
fig.suptitle('Munich: Average prices on '+company.title()+' stations in October 2022 by day of the week')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), loc="lower center", ncol=5)

# setting the axes labels and legend


# maximize the preview window 
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

#plt.show()


# saving the plot
plt.rcParams["figure.figsize"] = [8, 20] # the size of the figure to be saved
save_name = './samples/'+company+'_stations_MUC_Oct_by_dow.pdf'
plt.gcf().set_size_inches(8, 20)
fig.savefig(save_name, dpi = 400, format='pdf', orientation='landscape')
print('Saved: ' + save_name)

