import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
MUC_data = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')


test_id = 12404
verdi1_id = 12365 #agip
verdi2_id = 12366 #jet


string = input("Date: ")


date = string+'oct2022'


def getData(loc_id):

	# gets 'id_data' of a station based on 'location_id'
	i_d = MUC_char.loc[MUC_char[MUC_char['location_id'] == loc_id].index[0]].at['id_data']
	temp = MUC_data.loc[(MUC_data['id_data'] == i_d) & (MUC_data['date'] == date)]
	temp = temp.iloc[:, 4:]
	r = temp.to_numpy()
	r = r[0].tolist()
	return r



#id_data = MUC_char.loc[MUC_char[MUC_char['location_id'] == location_id].index[0]].at['id_data']
#id_data_verdi1 = MUC_char.loc[MUC_char[MUC_char['location_id'] == verdi1_id].index[0]].at['id_data']
#id_data_verdi2 = MUC_char.loc[MUC_char[MUC_char['location_id'] == verdi2_id].index[0]].at['id_data']


#data = MUC_data.loc[(MUC_data['id_data'] == id_data) & (MUC_data['date'] == date)]
#data = data.iloc[:, 4:]


#data_verdi1 = MUC_data.loc[(MUC_data['id_data'] == id_data_verdi1) & (MUC_data['date'] == date)]
#data_verdi1 = data_verdi1.iloc[:, 4:]

#data_verdi2 = MUC_data.loc[(MUC_data['id_data'] == id_data_verdi2) & (MUC_data['date'] == date)]
#data_verdi2 = data_verdi2.iloc[:, 4:]



#rangeY = data.to_numpy()
#rangeY = rangeY[0].tolist()


#rangeVerdi1 = data_verdi1.to_numpy()
#rangeVerdi1 = rangeVerdi1[0].tolist()

rangeVerdi1 = getData(verdi1_id)
rangeVerdi2 = getData(verdi2_id)




rangeX = range(0, 204)


#print(id_data)
#print(rangeY)

plt.rcParams["figure.figsize"] = [14, 8]
#plt.rcParams["figure.autolayout"] = True

#plt.plot(rangeX, rangeY)
plt.plot(rangeX, rangeVerdi1, label="Agip")
plt.plot(rangeX, rangeVerdi2, label="Jet")
plt.ylabel('Price in Euro')
plt.legend(loc="upper right")
plt.title('Munich: Verdistrasse 141 (Agip) vs. Verdistrasse 142 (Jet) on Oct '+string+' 2022')

frame1 = plt.gca()
frame1.set_ylim([1.90, 2.17])
frame1.axes.get_xaxis().set_visible(False)

manager = plt.get_current_fig_manager()
manager.window.showMaximized()

#plt.show()
plt.savefig('./samples/verdi_'+date+'.png', dpi = 150)

