import pandas as pd
from datetime import datetime
import re

# --- 1) stations' characteristics

# load the data file with stations' characteristics
#df_char = pd.read_csv('../data/stations_characteristics_MUC_long.csv')
df_char = pd.read_csv('../data/stations_characteristics_all_long.csv')

# change format of dates from string to datetime
df_char['first'] = pd.to_datetime(df_char['first'], format='%Y-%m-%d')
#df_char['first'] = pd.to_datetime(df_char['first'], format='%d%b%Y')
df_char['last'] = pd.to_datetime(df_char['last'], format='%Y-%m-%d')
#df_char['last'] = pd.to_datetime(df_char['last'], format='%d%b%Y')


# --- 2) stations' prices in matrix format (rows: dates x 'id_data', columns: 6:00, 6:05, 6:10, etc.)

# load the data file with prices
df_prices = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')
#df_prices = pd.read_csv('../data/stations_prices_all_wide_10-2022.csv')

# change format of dates from string to datetime
df_prices['date'] = pd.to_datetime(df_prices['date'], format='%d%b%Y')


# --- 3) stations' prices in list format (rows: 'id_data' x 'timestamp', column: 'price')

# load the data file with prices
df_linreg_prices = pd.read_csv('../data/stations_prices_list-fmt_MUC_10-2022.csv')


# --- 4) list of price increases by station - timestamp, post-change price, change amount, cycle, etc.

#df_price_inc = pd.read_csv('../data/price-increases_MUC_Oct22_price-leaders.csv')
df_price_inc = pd.read_csv('../data/price-increases_all-DE_10-2022_price-leaders.csv')


# --- 5) list of stations per day with mean price, price at 17h, etc & control variables for each station

#df_daily_station_linreg = pd.read_csv('../data/stations_prices_MUC_10-2022_station-reg.csv')
df_daily_station_linreg = pd.read_csv('../data/regression_stations_all_DE_Oct-Dec-2022.csv')
#df_daily_station_linreg = pd.read_csv('../data/stations_prices_all_DE_10-2022_station-reg.csv')


# --- 6) share of first movership by brand for each cluster 

df_share_first_movers = pd.read_csv('../data/share_first_movers_all-DE_group85.csv')


# ----- UTIL -----

# convert "p_e5_6oclock_0min" to 6:00
def convertTimestamp(string):
	hour_match = re.search(r"\d{1,2}oclock", string)
	minute_match = re.search(r"\d{1,2}min", string)

	if hour_match and minute_match:
		hour = int(hour_match.group()[:-6])
		minute = int(minute_match.group()[:-3])

		time = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
		return time

	return None  # Return None if the string format doesn't match


# change the column names for timestamps from "p_e5_6oclock_0min" to 6:00 (datetime type)
for column in df_prices.columns:
    if column.startswith('p_'): 
    	new_name = convertTimestamp(column)
    	df_prices.rename(columns={column: new_name}, inplace=True)


# check if columns are in chronological order
for i in range(0, len(df_prices.columns)-1):
	if isinstance(df_prices.columns[i], str):
		pass
	else:
		assert (df_prices.columns[i] <= df_prices.columns[i + 1]), "Timestamp columns are not in chronological order. Problem at: " + str(df_prices.columns[i])
