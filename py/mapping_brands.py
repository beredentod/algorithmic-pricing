import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import random


import stations_colors as sc

# https://towardsdatascience.com/plotting-maps-with-geopandas-428c97295a73


path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp'

stations_file = '../data/stations_characteristics_MUC_long.csv'

verdi1_id = 12365 #agip
verdi2_id = 12366 #jet



# Read in and filter (see documentation)
gdf_roads = geopds.read_file(path + file)
#gdf_highways = gdf_roads.loc[gdf_roads['BEZ'].str[0].isin(['A','E'])]


# Read in gas station data and transform from pandas dataframe to geopandas dataframe
df_stations = pd.read_csv(stations_file)
gdf_stations = geopds.GeoDataFrame(df_stations, geometry=geopds.points_from_xy(df_stations.longitude, df_stations.latitude, crs="EPSG:3035")) # Correct projection for Lat/Long

brands = gdf_stations['brand_id'].unique()

brands_stations = []

for i in brands:
	brands_stations.append(gdf_stations[(gdf_stations['brand_id'] == i)])




# Visualize: https://geopandas.org/en/stable/docs/user_guide/mapping.html
fig, ax = plt.subplots(figsize=(15, 15))


# whole Munich
ax.set_xlim([11.39, 11.73])
ax.set_ylim([48.06, 48.225])

ax.set_title('Gas stations in Munich')

#print(gdf_stations)

gdf_roads.to_crs(epsg=4326).plot(ax=ax,color='grey', zorder=10) # Roads layer'''

colors = ['black', 'rosybrown', 'brown', 'maroon', 'red', 'orange', 'darkgoldenrod', 
'olive', 'yellow', 'peru', 'lawngreen', 'lime', 'turquoise', 'darkslategrey', 'dodgerblue',
'blue', 'indigo',  'purple', 'deeppink', 'crimson']

print(colors)

for idx, val in enumerate(brands_stations):
	val.plot(ax=ax, label=brands[idx], zorder= 100, color=colors[idx])





ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')
ax.legend(loc="lower right", ncol=4)

plt.show()


print("success")