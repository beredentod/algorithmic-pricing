import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd


MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


# returns the list of 'id_data' for each station within the brand
def getStationsbyCompany(comp_name):
	stations = MUC_char[MUC_char['brand_id'] == comp_name]
	ids = stations['id_data'].tolist()
	return ids


# get time series of prices for one particular station (based on 'id_data') and a date
def getDataSingleStation(local_id_data, local_date):
	temp = MUC_data.loc[(MUC_data['id_data'] == local_id_data) & (MUC_data['date'] == local_date)]

	# if the data set includes the given station for the given date
	if not temp.empty:
		temp = temp.iloc[:, 4:]  # takes the 4th column onwards ('6:00', '6:05', ...)
		r = temp.to_numpy()
		r = r[0]
		return r

	# returns None if there is no data for the given station on the given date
	return 





string = input("Date: ")
date = string+'oct2022'
company = 'bavaria petrol'



# list of 'id_data' for $company
stations = getStationsbyCompany(company)





ranges = []
ids = []

avg = []

for s in stations:
	ret = getDataSingleStation(s, date)
	if ret is not None:
		ranges.append(ret)
		ids.append(s)

print(ranges)


# calculate average for one company

for idx, val in enumerate(ranges[1]):
	temp_sum = 0
	for rr in ranges:
		temp_sum += rr[idx]
	temp_sum /= len(ranges)
	avg.append(temp_sum)

print(avg)



# create labels for the graph as "street & no. "

names = []

for x in ids:
	street = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['street']
	house_number = MUC_char.loc[MUC_char[MUC_char['id_data'] == x].index[0]].at['house_number']
	names.append(str(street) + " " + str(house_number))


ranges.append(avg)
names.append("AVERAGE")


print(names)


minv = 1000
maxv = 0

print(MUC_data.iloc[:, 4:].min().min())

print (minv, maxv)

for i in range(1, 31):
	if i < 10:
		loc_date = '0' + str(i) + "oct2022" 
	else:
		loc_date = str(i) + "oct2022" 

	for s in stations:
		ret = getDataSingleStation(s, loc_date)
		if ret is not None:
			for j in ret:
				minv = min(minv, j)
				maxv = max(maxv, j)
	

low = minv
high = maxv



times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
#print(times)

rangeX = times

myFmt = mdates.DateFormatter('%H:%M')


#print(id_data)
#print(rangeY)

plt.rcParams["figure.figsize"] = [14, 8]

fig, ax = plt.subplots()
#ax2 = ax1.twinx()


for idx, rr in enumerate(ranges):
	ax.plot_date(rangeX, rr, label=names[idx], marker='', linestyle='-')

#ax1.plot_date(rangeX, getData(verdi1_id, '03oct2022'), 'b', label="03.10.2022", marker='', linestyle='-')
#ax2.plot_date(rangeX, getData(verdi1_id, '10oct2022'), 'g', label="10.10.2022", marker='', linestyle='-')


ax.xaxis.set_major_formatter(myFmt)


ax.set_ylim(low, high)


#plt.rcParams["figure.autolayout"] = True

#plt.plot(rangeX, rangeY)
#plt.plot_date(rangeX, rangeVerdi1, label="Agip")
#plt.plot_date(rangeX, rangeVerdi2, label="Jet")

ax.set_ylabel('Price in Euro')
ax.set_title('Munich: '+company.title()+' stations on Oct '+string+' 2022')
ax.legend(loc="lower center", ncol=5)
#ax2.legend(loc="upper left")



#frame1 = plt.gca()
#frame1.set_ylim([1.90, 2.17])
#frame1.axes.get_yaxis().set_visible(False)

manager = plt.get_current_fig_manager()
manager.window.showMaximized()

plt.show()


#fig.savefig('./samples/'+company+'_stations_MUC_'+date+'.png', dpi = 400)
#print('Saved: ' + './samples/'+company+'_stations_MUC_'+date+'.png')

