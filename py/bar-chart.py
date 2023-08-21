'''
File: bar-chartt.py
- yields a vertical bar chart with the number of stations within Munich for each brand
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd

import stations_colors as sc


# import the stations data
MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


#count stations by brand
counts = {}

for item in MUC_char['brand_id']:
    if item not in counts:
        counts[item] = 1
    else:
        counts[item] += 1


# sort items by value in reversed order
counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

rangeX = list(counts.keys()) # names of the brands
rangeY = list(counts.values()) # values = number of stations per brand


# move 'sonstige' to the back of the chart
if 'sonstige' in rangeX:
	ind = int(rangeX.index('sonstige'))
	temp = rangeY[ind]

	del rangeX[ind]
	del rangeY[ind]

	rangeX.append('sonstige')
	rangeY.append(temp)


# make the size of the saved figure larger
plt.rcParams["figure.figsize"] = [14, 8]


# create the figure
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(1, 1, 1)


# generate the plot
bars = ax.bar(rangeX, rangeY)


#rotate the label for each bar, as they overlap
plt.xticks(rotation=45, ha='right')
ax.bar_label(bars)


# set the color of each bar to the brand's color
for index, value in enumerate(rangeY):
	bars[index].set_color(sc.hex_to_rgb(sc.colors_brands[rangeX[index]]))


# set title of the graph
ax.set_title('Gas stations in Munich by brand, May 2023')


# make the plt winodow maximized
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

plt.show()

# save file
fig.savefig('../plots/barchart_stations_Munich', dpi = 150)
print('Saved: ' + '../plots/barchart_stations_Munich.png')










'''

def getData(loc_id, local_date = date):

	# gets 'id_data' of a station based on 'location_id'
	i_d = MUC_char.loc[MUC_char[MUC_char['location_id'] == loc_id].index[0]].at['id_data']
	temp = MUC_data.loc[(MUC_data['id_data'] == i_d) & (MUC_data['date'] == local_date)]
	temp = temp.iloc[:, 4:]
	r = temp.to_numpy()
	r = r[0]
	return r


rangeVerdi1 = getData(verdi1_id)
rangeVerdi2 = getData(verdi2_id)


times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
#print(times)

rangeX = times

myFmt = mdates.DateFormatter('%H:%M')


#print(id_data)
#print(rangeY)

plt.rcParams["figure.figsize"] = [14, 8]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()


#ax1.plot_date(rangeX, rangeVerdi1, 'b', label="Agip", marker='', linestyle='-')
#ax2.plot_date(rangeX, rangeVerdi2, 'tab:orange', label="Jet", marker='', linestyle='-')

ax1.plot_date(rangeX, getData(verdi1_id, '03oct2022'), 'b', label="03.10.2022", marker='', linestyle='-')
ax2.plot_date(rangeX, getData(verdi1_id, '10oct2022'), 'g', label="10.10.2022", marker='', linestyle='-')


ax1.xaxis.set_major_formatter(myFmt)

low = 1.87
high = 2.17

ax1.set_ylim(low, high)
ax2.set_ylim(low, high)

#plt.rcParams["figure.autolayout"] = True

#plt.plot(rangeX, rangeY)
#plt.plot_date(rangeX, rangeVerdi1, label="Agip")
#plt.plot_date(rangeX, rangeVerdi2, label="Jet")

ax1.set_ylabel('Price in Euro')
#ax1.set_title('Munich: Verdistrasse 141 (Agip) vs. Verdistrasse 142 (Jet) on Oct '+string+' 2022')
ax1.legend(loc="upper right")
ax2.legend(loc="upper left")



frame1 = plt.gca()
#frame1.set_ylim([1.90, 2.17])
frame1.axes.get_yaxis().set_visible(False)

manager = plt.get_current_fig_manager()
manager.window.showMaximized()

plt.show()
#fig.savefig('./samples/verdi_'+date+'.png', dpi = 150)
#print('Saved: ' + './samples/verdi1_compare_'+date+'.png') '''

