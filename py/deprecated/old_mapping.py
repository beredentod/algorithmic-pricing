import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt

# https://towardsdatascience.com/plotting-maps-with-geopandas-428c97295a73


path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp'

stations_file = '../data/stations_characteristics_MUC_long.csv'

# Read in and filter (see documentation)
gdf_roads = geopds.read_file(path + file)
#gdf_highways = gdf_roads.loc[gdf_roads['BEZ'].str[0].isin(['A','E'])]

# Read in gas station data and transform from pandas dataframe to geopandas dataframe
df_stations = pd.read_csv(stations_file)
gdf_stations = geopds.GeoDataFrame(df_stations, geometry=geopds.points_from_xy(df_stations.longitude, df_stations.latitude, crs="EPSG:3035")) # Correct projection for Lat/Long
#gdf_stations = gdf_stations.to_crs(epsg=3035) # Project to metric system
#gdf_stations = gdf_stations.to_crs(epsg="EPSG:3035") # Project to metric system


# Calculate distance matrix (can take a long time, so potentially split dataset into regional clusters)
#for ind in gdf_stations.index:
#      geometry_i = gdf_stations['geometry'].loc[ind]
#           gdf_stations['distance_i'] = gdf_stations.distance(geometry_i)


# Visualize: https://geopandas.org/en/stable/docs/user_guide/mapping.html
fig, ax = plt.subplots(figsize=(15, 15))

# whole Munich
ax.set_xlim([11.39, 11.73])
ax.set_ylim([48.06, 48.225])

#verdistrasse
#ax.set_xlim([11.44, 11.48])
#ax.set_ylim([48.16, 48.17])

ax.set_title('Gas stations in Munich')
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')
ax.legend(loc="lower right", ncol=4)

gdf_stations.plot(ax=ax, alpha=1, color="red") # Station layer
gdf_roads.to_crs(epsg=4326).plot(ax=ax,color='grey') # Roads layer'''


plt.show()


print("success")