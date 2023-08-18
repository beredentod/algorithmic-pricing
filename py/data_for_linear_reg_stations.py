import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import re

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


# return the brand of the station based on id_data
def lookupBrand(id_data):
	return MUC_char.loc[MUC_char['id_data'] == id_data, 'brand_id'].iloc[0]


# return the address of the station based on id_data
def lookupAddress(id_data):
	street = MUC_char.loc[MUC_char['id_data'] == id_data, 'street'].iloc[0]
	house_number = MUC_char.loc[MUC_char['id_data'] == id_data, 'house_number'].iloc[0]
	post_code = MUC_char.loc[MUC_char['id_data'] == id_data, 'post_code'].iloc[0]

	return(street + " " + str(house_number) + ", " + str(post_code))

# convert "22oct2022" to datetime type
def convertDate(str_date):
	format = "%d%b%Y"
	return datetime.strptime(str_date, format)

# convert "p_e5_6oclock_0min" to 6:00
def convertTime(string):
	hour_match = re.search(r"\d{1,2}oclock", string)
	minute_match = re.search(r"\d{1,2}min", string)

	if hour_match and minute_match:
		hour = int(hour_match.group()[:-6])
		minute = int(minute_match.group()[:-3])

		time = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
		return time

	return None  # Return None if the string format doesn't match


'''
Table with 

( id ) | Tankstelle_id id_data | company | time t | price P_i,t | dummy_Mon | dummy_Tue | ... | dummy_Sun

'''


# let's examine Aral first
company = 'total'


df = pd.DataFrame(columns = ['id_data', 'brand', 'time', 'P_it', 'dummy_Mon', 'dummy_Tue', 'dummy_Wed', 'dummy_Thu', 'dummy_Fri', 'dummy_Sat', 'dummy_Sun'])

stations = getStationsbyCompany(company)
todo_rows = MUC_data[MUC_data['id_data'].isin(stations)]



for index, row in todo_rows.iterrows():
	date = convertDate(row['date']) # converts date to type datetime
	brand = lookupBrand(row['id_data']) # looks up brand_id
	dow = date.weekday() # 0 - 6 (Mon - Sun)


	for idx, val in enumerate(row[4:], start = 4):
		my_list = [0] * (4+7)
		my_list[0] = row[0]
		my_list[1] = brand 
		my_list[2] = datetime.combine(date, convertTime(todo_rows.columns[idx]))
		my_list[3] = val
		my_list[4+dow] = 1 # insert dummy value

		df.loc[len(df)] = my_list # add to the dataframe

df = df.dropna()

print(df)


string = '../data/MUC_oct22_Total.csv'
df.to_csv(string, index=False)
print('File ' + string + ' was saved.')


print(lookupAddress(getStationsbyCompany(company)[0]))


# for brands
'''
df = pd.read_csv('../data/MUC_oct22_aggregate.csv')

df = df.drop(columns=['dummy_Mon', 'dummy_Tue', 'dummy_Wed', 'dummy_Thu', 'dummy_Fri', 'dummy_Sat', 'dummy_Sun'])


a = [
'agip', 'allguth', 'aral', 'avia', 'bavaria petrol', 'bk', 'esso', 'jet', 'mr wash', 'oil!',
 'omv', 'shell', 'sprint', 'star', 'sued treibstoff', 'total', 'v-markt', 'sonstige']

for x in a:
	df[x] = 0


for x in a:
	df.loc[df['brand'] == x, x] = 1	


print (df)

string = '../data/MUC_oct22_brand-dummies_aggregate.csv'
df.to_csv(string, index=False)
print('File ' + string + ' was saved.')

'''




'''
df = pd.read_csv('../data/MUC_oct22_aggregate.csv')

df = df.drop(columns=['dummy_Mon', 'dummy_Tue', 'dummy_Wed', 'dummy_Thu', 'dummy_Fri', 'dummy_Sat', 'dummy_Sun'])

def datetime_to_number(dt_str):
    base_time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    start_time = datetime(base_time.year, base_time.month, base_time.day, 6, 0)  # Start time at 6:00
    end_time = datetime(base_time.year, base_time.month, base_time.day, 23, 0)  # End time at 23:00
    interval = timedelta(minutes=5)  # 5-minute intervals

    if base_time < start_time or base_time > end_time:
        raise ValueError("Datetime is outside the valid range (6:00 - 23:00)")

    diff = base_time - start_time
    minutes = diff.total_seconds() // 60

    number = int(minutes // 5)
    return number


df['timestamp'] = 0
df['timestamp'] = df['time'].apply(datetime_to_number)


print(df)


string = '../data/MUC_oct22_timestamps-dummies_aggregate.csv'
df.to_csv(string, index=False)
print('File ' + string + ' was saved.')
'''




'''
agip = pd.read_csv('../data/MUC_oct22_Agip.csv')
allguth = pd.read_csv('../data/MUC_oct22_Allguth.csv')
aral = pd.read_csv('../data/MUC_oct22_Aral.csv')
esso = pd.read_csv('../data/MUC_oct22_Esso.csv')
jet = pd.read_csv('../data/MUC_oct22_Jet.csv')
omv = pd.read_csv('../data/MUC_oct22_OMV.csv')
shell = pd.read_csv('../data/MUC_oct22_Shell.csv')
total = pd.read_csv('../data/MUC_oct22_Total.csv')

avia = pd.read_csv('../data/MUC_oct22_Avia.csv')
bavaria_petrol = pd.read_csv('../data/MUC_oct22_Bavaria_Petrol.csv')
sprint = pd.read_csv('../data/MUC_oct22_Sprint.csv')
v_markt = pd.read_csv('../data/MUC_oct22_V-Markt.csv')
bk = pd.read_csv('../data/MUC_oct22_BK.csv')
sued_treibstoff = pd.read_csv('../data/MUC_oct22_Sued_Treibstoff.csv')
oil = pd.read_csv('../data/MUC_oct22_Oil!.csv')
mr_wash = pd.read_csv('../data/MUC_oct22_Mr_Wash.csv')
star = pd.read_csv('../data/MUC_oct22_Star.csv')
sonstige = pd.read_csv('../data/MUC_oct22_Sonstige.csv')


concatenated_df = pd.concat([agip, allguth, aral, esso, jet, omv, shell, total, 

avia,
bavaria_petrol,
sprint,
v_markt,
bk,
sued_treibstoff,
oil,
mr_wash,
star,
sonstige

	], ignore_index=True)

concatenated_df.to_csv('../data/MUC_oct22_aggregate.csv', index=False)
'''






