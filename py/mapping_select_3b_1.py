import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt

from functions_1 import df_char

path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp'

# Read in and filter (see documentation)
gdf_roads = geopds.read_file(path + file)




fig, ax = plt.subplots(figsize=(15, 15))

df_char['bool_selected'] = 0

#ids = ['0abaccf2-5efa-4536-b5c5-afe3932e3724', '0c3b710a-3aae-45c9-998d-e0783ef83b60', '2acc4724-ea6a-4874-baa6-e191ccb12756',
#'5342d82a-fefd-44c8-a59d-be8111fdb867', '5c97286d-228e-4def-8d30-2c2f63668b92', 'dba3e2af-0314-4c39-9a13-57244fdeb47d']

clusters = [4, 7, 9, 18, 20, 23, 24, 25, 26, 29, 33, 37]


#df_char.loc[df_char['id_data_updated'].isin(ids), 'bool_selected'] = 1
df_char.loc[df_char['group80'].isin(clusters), 'bool_selected'] = 1




unselected = df_char[df_char['bool_selected'] == 0]
group_stations = geopds.GeoDataFrame(unselected, geometry=geopds.points_from_xy(unselected.longitude, unselected.latitude, crs="EPSG:3035"))
group_stations.plot(ax=ax, alpha=1, zorder=100, color='blue')

selected = df_char[df_char['bool_selected'] == 1]
group_stations = geopds.GeoDataFrame(selected, geometry=geopds.points_from_xy(selected.longitude, selected.latitude, crs="EPSG:3035"))
group_stations.plot(ax=ax, alpha=1, zorder=100, color='grey')


gdf_roads.to_crs(epsg=4326).plot(ax=ax,color='lightgrey') # Roads layer


for idx, row in selected.iterrows():
	ax.annotate(row['group80'], xy=(row['longitude']+0.002,row['latitude']+0.002), color='black', horizontalalignment="center")



# whole Munich
ax.set_xlim([11.39, 11.73])
ax.set_ylim([48.06, 48.225])

#verdistrasse
#ax.set_xlim([11.44, 11.48])
#x.set_ylim([48.16, 48.17])


ax.set_title('Gas stations in Munich, selected: cluster85 with at least one Aral or Shell station')
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')
ax.legend(loc="lower right", ncol=4)


plt.show()

print("success")
