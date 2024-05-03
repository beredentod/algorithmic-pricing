'''
File: util_linreg_03.py

- convert stations' prices in matrix format to list format (i.e. each row with price for each timestamp)
'''

import pandas as pd
from datetime import datetime

import functions_1 as fcs

start_date = datetime(2022, 10, 1)
end_date = datetime(2022, 10, 31)

df_prices = fcs.selectPriceAllRowsRange(start_date, end_date, id_data_updated = True)

print(df_prices)

# create dataframe with prices in list format 
df_linreg_prices = fcs.createTableForLinReg(df_prices)

print(df_linreg_prices)

filename = '../data/stations_prices_linreg_MUC_10-2022.csv'
#merged_df.to_csv(filename, index=False)
#print('Saved! ' + filename)