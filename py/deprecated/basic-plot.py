import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd


MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


test_id = 12404
verdi1_id = 12365 #agip
verdi2_id = 12366 #jet

omv1 = 12334
omv2 = 12335

omv3 = 12367

sprint = 12341

sprintID = '867a2e12-b0ae-4386-8c62-a5e1593e83f6'
sprint2ID = '01286f59-0bf7-4d9c-be8d-ee5683239021'


string = input("Date: ")
date = string+'oct2022'

#date = '03oct2022'


def getData(loc_id, local_date = date):

	# gets 'id_data' of a station based on 'location_id'
	i_d = MUC_char.loc[MUC_char[MUC_char['location_id'] == loc_id].index[0]].at['id_data']
	temp = MUC_data.loc[(MUC_data['id_data'] == i_d) & (MUC_data['date'] == local_date)]
	temp = temp.iloc[:, 4:]
	r = temp.to_numpy()
	r = r[0]
	return r


def getDataIdData(id_data, local_date = date):

	# gets 'id_data' of a station based on 'location_id'
	temp = MUC_data.loc[(MUC_data['id_data'] == id_data) & (MUC_data['date'] == local_date)]
	temp = temp.iloc[:, 4:]
	r = temp.to_numpy()
	r = r[0]
	return r



times = (pd.date_range("6:00", "22:55", freq="5min")).to_numpy()
#print(times)

rangeX = times



#print(id_data)
#print(rangeY)

plt.rcParams["figure.figsize"] = [14, 8]

fig, ax = plt.subplots()


#ax1.plot_date(rangeX, rangeVerdi1, 'b', label="Agip", marker='', linestyle='-')
#ax2.plot_date(rangeX, rangeVerdi2, 'tab:orange', label="Jet", marker='', linestyle='-')

#ax.plot_date(rangeX, getData(12365, date), label="agip", marker='', linestyle='-')
#ax.plot_date(rangeX, getData(12366, date), label="jet", marker='', linestyle='-')
#ax.plot_date(rangeX, getData(12367, date), label="omv", marker='', linestyle='-')
#ax.plot_date(rangeX, getData(12368, date), label="shell", marker='', linestyle='-')


ax.plot_date(rangeX, getData(omv1, date), label="OMV - freisinger landstrasse 26", fmt='')
ax.plot_date(rangeX, getData(omv2, date), label="OMV - freisinger landstrasse 9", fmt='')
ax.plot_date(rangeX, getData(omv3, date), label="OMV - control", fmt='')
#ax.plot_date(rangeX, getDataIdData(sprintID, date), label="Sprint - situlistrasse 36", fmt='')
#ax.plot_date(rangeX, getDataIdData(sprint2ID, date), label="Sprint2", fmt='')



#examine = getData(12368, date)
times = (pd.date_range("6:00", "22:55", freq="5min"))

#result_dict = dict(zip(times, examine))

#print(result_dict)



# setting the date format of the x-axis labels
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)


# setting the boundaries of the y-axis
low = 1.7875
high = 2.2215
ax.set_ylim(low, high)


# setting the axes labels and legend
ax.set_ylabel('Price in Euro')
ax.set_title('Munich: Stations at Freisinger Landstrasse on ' + date)
ax.legend(loc="lower center", ncol=5)


# maximize the preview window 
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

plt.show()


# saving the plot
plt.rcParams["figure.figsize"] = [14, 8] # the size of the figure to be saved
savefile = './samples/freisinger_landstrasse_stations_MUC_'+date+'.png'
fig.savefig(savefile, dpi = 400)
print('Saved: ' + savefile)


