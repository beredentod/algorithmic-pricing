import geopandas as geopds
import pandas as pd
import matplotlib.pyplot as plt
import stations_colors as sc

from functions_1 import df_char

path = './'

# Relevante Datei
file = 'dlm250.utm32s.shape.ebenen/dlm250_ebenen/geb01_f.shp' #gebiet

# Read in and filter (see documentation)
gdf_map = geopds.read_file(path + file)

gdf_map = gdf_map[gdf_map['OBJART_TXT'] == 'AX_Gebiet_Kreis']



fig, ax = plt.subplots(figsize=(9, 16))

brand = 'shell'


df_char = df_char[df_char['brand_id'] == brand]
gdf_stations = geopds.GeoDataFrame(df_char, geometry=geopds.points_from_xy(df_char.longitude, df_char.latitude, crs="EPSG:3035"))
gdf_stations.plot(ax=ax, alpha=1, zorder=100, color=sc.hex_to_rgb(sc.colors_brands[brand]), edgecolor='black') # Station layer



'''
grouped = df_char.groupby(cluster)


for name, group in grouped:
	group_stations = geopds.GeoDataFrame(group, geometry=geopds.points_from_xy(group.longitude, group.latitude, crs="EPSG:3035"))
	group_stations.plot(ax=ax, alpha=1, zorder=100)'''


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

#plt.show()

print("success")


save_name = f'./samples/map_germany_'+brand+'.pdf'

# save figure to a file
fig.savefig(save_name, format='pdf', bbox_inches='tight')
#fig.savefig(f'./samples/map_germany_'+brand+'.png', dpi = 150)
print('Saved: ' + save_name)



