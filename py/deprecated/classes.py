from datetime import datetime

class Price:
	def __init__(self, value, timestamp):
		self.value = value
		if isinstance(timestamp, datetime):
			self.time = timestamp
		else:
			raise ValueError("Timestamp for a Price object must be a datetime object.")

	def get_formatted_timestamp(self):
		return self.time.strftime("%d-%m-%Y %H:%M")

	def __str__(self):
		return f"price: {self.value}\ntime: {self.get_formatted_timestamp()}"


class Station:
	def __init__(self, location_id):
		self.id_data = None
		self.brand_id = None
		self.cluster = None # group85
		self.location_id = location_id
		self.address = None
		self.latitude = None
		self.longitute = None

	def __str__(self):
		return f"{self.location_id}, {self.brand_id}, {self.address}"




