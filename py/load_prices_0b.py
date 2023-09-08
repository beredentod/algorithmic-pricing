import pandas as pd
from datetime import datetime
import re


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


# load the data file with prices
df_prices = pd.read_csv('../data/stations_prices_MUC_wide_10-2022.csv')

# change format of dates from string to datetime
df_prices['date'] = pd.to_datetime(df_prices['date'], format='%d%b%Y')


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

