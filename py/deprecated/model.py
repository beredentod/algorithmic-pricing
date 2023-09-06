import classes as ap
import pandas as pd

class Model:
	def __init__(self):
		self.stations = []


	def loadStations(self, path):	
		df_char = pd.read_csv(path)
		for index, row in df_char.iterrows():
			station_id = row['location_id']

			station = ap.Station(station_id)
			self.stations.append(station)


	def loadPrices():
		#
		return




#MUC_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')

M = Model()
M.loadStations('../data/stations_characteristics_MUC_long.csv')



