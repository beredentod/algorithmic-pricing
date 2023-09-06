import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt

from compilation import df_stations

path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp'

# Read in and filter (see documentation)
gdf_roads = geopds.read_file(path + file)

# Correct projection for Lat/Long

#gdf_stations = geopds.GeoDataFrame(df_stations, geometry=geopds.points_from_xy(df_stations.longitude, df_stations.latitude, crs="EPSG:3035")) 

cluster = 'group90'

fig, ax = plt.subplots(figsize=(15, 15))


grouped = df_stations.groupby(cluster)


for name, group in grouped:
	group_stations = geopds.GeoDataFrame(group, geometry=geopds.points_from_xy(group.longitude, group.latitude, crs="EPSG:3035"))
	group_stations.plot(ax=ax, alpha=1, zorder=100)


#gdf_stations.plot(ax=ax, alpha=1, color="red") # Station layer
gdf_roads.to_crs(epsg=4326).plot(ax=ax,color='grey') # Roads layer


for idx, row in df_stations.iterrows():
	ax.annotate(row[cluster], xy=(row['longitude']+0.002,row['latitude']+0.002), color='black', horizontalalignment="center")



# whole Munich
ax.set_xlim([11.39, 11.73])
ax.set_ylim([48.06, 48.225])

#verdistrasse
#ax.set_xlim([11.44, 11.48])
#x.set_ylim([48.16, 48.17])


ax.set_title('Gas stations in Munich, cluster: ' + cluster)
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')
ax.legend(loc="lower right", ncol=4)


plt.show()

print("success")