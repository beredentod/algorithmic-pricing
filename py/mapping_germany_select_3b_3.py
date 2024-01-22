import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt
import stations_colors as sc

import functions_1 as fcs
from functions_1 import df_price_inc
from functions_1 import df_char

path = './'

# Relevante Datei
#file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/ver01_l.shp' #verkehr
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/geb01_f.shp' #gebiet

# Read in and filter (see documentation)
gdf_map = geopds.read_file(path + file)

gdf_map = gdf_map[gdf_map['OBJART_TXT'] == 'AX_Gebiet_Kreis']


# Correct projection for Lat/Long

#gdf_stations = geopds.GeoDataFrame(df_char, geometry=geopds.points_from_xy(df_char.longitude, df_char.latitude, crs="EPSG:3035")) 

#cluster = 'group90'

fig, ax = plt.subplots(figsize=(15, 15))

brand = 'total'

'''

df_char_filtered = df_char[df_char['brand_id'] == brand]

df_char_filtered.reset_index(drop=True, inplace=True)

df_price_inc = df_price_inc[df_price_inc['brand_id'] == brand]

df_price_inc = df_price_inc[df_price_inc['cycle'] == 4]

print(df_price_inc)

count_by_date = df_price_inc.groupby('date')['id_data_updated'].nunique()
print(count_by_date)
count_by_station = df_price_inc['id_data_updated'].value_counts()
pd.set_option('display.max_rows', None)
print(count_by_station)

ids_to_save = count_by_station[count_by_station < 3].index.tolist()

n = df_price_inc['id_data_updated'].nunique()
print(f'# of {brand} stations: {n}')

print(fcs.lookUpAddress('a6b5d41e-de7b-4aa3-aad7-5727edfaf777'))



#gdf_stations = geopds.GeoDataFrame(df_char, geometry=geopds.points_from_xy(df_char.longitude, df_char.latitude, crs="EPSG:3035"))
#gdf_stations.plot(ax=ax, alpha=1, zorder=100, color=sc.hex_to_rgb(sc.colors_brands[brand]), edgecolor='black') # Station layer


df_char_filtered['bool_selected'] = 0
df_char_filtered.loc[df_char_filtered['id_data_updated'].isin(ids_to_save), 'bool_selected'] = 1

print(df_char_filtered['bool_selected'].value_counts())


unselected = df_char_filtered[df_char_filtered['bool_selected'] == 0]
group_stations = geopds.GeoDataFrame(unselected, geometry=geopds.points_from_xy(unselected.longitude, unselected.latitude, crs="EPSG:3035"))
group_stations.plot(ax=ax, alpha=1, zorder=100, color='grey', edgecolor='black')

selected = df_char_filtered[df_char_filtered['bool_selected'] == 1]
group_stations = geopds.GeoDataFrame(selected, geometry=geopds.points_from_xy(selected.longitude, selected.latitude, crs="EPSG:3035"))
group_stations.plot(ax=ax, alpha=1, zorder=100, color=sc.hex_to_rgb(sc.colors_brands[brand]), edgecolor='black')



grouped = df_char.groupby(cluster)


for name, group in grouped:
	group_stations = geopds.GeoDataFrame(group, geometry=geopds.points_from_xy(group.longitude, group.latitude, crs="EPSG:3035"))
	group_stations.plot(ax=ax, alpha=1, zorder=100)


#gdf_stations.plot(ax=ax, alpha=1, color="red") # Station layer
gdf_map.to_crs(epsg=4326).plot(ax=ax, color='white', edgecolor='grey') # Roads layer


#for idx, row in df_stations.iterrows():
#	ax.annotate(row[cluster], xy=(row['longitude']+0.002,row['latitude']+0.002), color='black', horizontalalignment="center")





ax.set_title('Fuel stations in Germany, brand: ' + brand)
ax.set_xticks([])
ax.set_yticks([])
#ax.set_ylabel('Latitude')
#ax.set_xlabel('Longitude')
#ax.legend(loc="lower right", ncol=4)

plt.tight_layout()

plt.show()

print("success")


#save_name = f'./samples/map_germany_'+brand+'.pdf'

# save figure to a file
#fig.savefig(save_name, format='pdf', bbox_inches='tight')
#fig.savefig(f'./samples/map_germany_'+brand+'.png', dpi = 150)
#print('Saved: ' + save_name)

'''