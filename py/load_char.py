import pandas as pd
from datetime import datetime


# load the data file with stations' characteristics
df_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')

# change format of dates from string to datetime
df_char['first'] = pd.to_datetime(df_char['first'], format='%d%b%Y')
df_char['last'] = pd.to_datetime(df_char['last'], format='%d%b%Y')



