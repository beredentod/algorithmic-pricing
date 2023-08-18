import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt

import stations_colors as sc

# https://towardsdatascience.com/plotting-maps-with-geopandas-428c97295a73


path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp'
file_MUC_char = '../data/stations_characteristics_MUC_long.csv'

MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


def getData(loc_id, local_date):

	# gets 'id_data' of a station based on 'location_id'
	i_d = MUC_char.loc[MUC_char[MUC_char['location_id'] == loc_id].index[0]].at['id_data']
	temp = MUC_data.loc[(MUC_data['id_data'] == i_d) & (MUC_data['date'] == local_date)]
	temp = temp.iloc[:, 4:]
	r = temp.to_numpy()
	r = r[0]
	return r


verdi1_id = 12365 #agip
verdi2_id = 12366 #jet
verdi3_id = 12367 #omv
verdi4_id = 12368 #shell

verdi = [12365, 12366, 12367, 12368]
names = ['agip', 'jet', 'omv', 'shell']


date = '03oct2022'


rangesVerdi = []
for i in verdi:
	rangesVerdi.append(getData(i, date))


adjustments = []	

for rr in rangesVerdi:
	temp_arr = [0]
	for i in range(1, 204):
		if (rr[i] > rr[i-1]):
			temp_arr.append(1)
		elif (rr[i] < rr[i-1]):
			temp_arr.append(-1)
		else:
			temp_arr.append(0)
	adjustments.append(temp_arr)

# Read in and filter (see documentation)
gdf_roads = geopds.read_file(path + file)


colors = ['grey', 'grey', 'grey', 'grey']

gdf_stations = geopds.GeoDataFrame(MUC_char, geometry=geopds.points_from_xy(MUC_char.longitude, MUC_char.latitude, crs="EPSG:3035")) # Correct projection for Lat/Long

gdf_verdi = []
for i in verdi:
	gdf_verdi.append(gdf_stations[gdf_stations['location_id'] == i])


times = (pd.date_range("6:00", "22:55", freq="5min"))
times = times.format(formatter=lambda x: x.strftime('%H:%M'))

fig, ax = plt.subplots(figsize=(15, 15))

#time = input("Insert time: ")


#t = ['06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35']
t = times
count = 2

gdf_roads.to_crs(epsg=4326).plot(ax=ax,color='black', zorder=1) # Roads layer'''


for i in t:

	idx_time = times.index(i)


	for idx, val in enumerate(colors):
		if adjustments[idx][idx_time] == 1:
			colors[idx] = 'red'
		elif adjustments[idx][idx_time] == -1:
			colors[idx] = 'blue'
		else:
			colors[idx] = 'grey'

	gdf_verdi[0].plot(ax=ax, color=colors[0], label='agip', zorder=count, markersize = 170) # Station layer
	gdf_verdi[1].plot(ax=ax, color=colors[1], label='jet', zorder=count, markersize = 170) # Station layer
	gdf_verdi[2].plot(ax=ax, color=colors[2], label='omv', zorder=count, markersize = 170) # Station layer
	gdf_verdi[3].plot(ax=ax, color=colors[3], label='shell', zorder=count, markersize = 170) # Station layer


	#verdistrasse
	ax.set_xlim([11.44, 11.48])
	ax.set_ylim([48.16, 48.17])
	ax.set_ylabel('Latitude')
	ax.set_xlabel('Longitude')
	#ax.legend(loc="lower right", ncol=4)

	ax.set_title('Gas stations in Munich Verdistrasse on ' +date+ ' at '+i)


	#plt.show()


	plt.rcParams["figure.figsize"] = [14, 8] # the size of the figure to be saved
	save_name = './samples/verdi/map_verdistrasse_MUC_'+date+'_'+i+'.png'
	plt.gcf().set_size_inches(14, 8)
	fig.savefig(save_name, dpi = 100, format='png', orientation='landscape')
	print('Saved: ' + save_name)


	count += 1