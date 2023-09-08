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