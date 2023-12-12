import pandas as pd
from load_char_0a import df_char

df_zip = pd.read_csv('../data/zip_controls.csv')

df_char = pd.merge(df_char, df_zip , on='post_code', how='inner')

print(df_char)

#df_char.to_csv('../data/stations_characteristics_MUC_long.csv', index = False)
#print('Saved!')