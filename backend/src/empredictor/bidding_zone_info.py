import datetime as dt
import pandas as pd

# THIS IS SUBJECT TO CHANGE AND NEEDS TO BE UPDATED ACCORDINGLY

# Only covered for Germany; the rest will follow sometime in the future
class Germany:
	def __init__(self):
		self.timezone_name = 'Europe/Berlin'
		self.hour_offset_to_UTC = 1
	def get_range(self):
		start = pd.Timestamp('20150101', tz=self.timezone_name)
		local_time = pd.Timestamp.now(tz=self.timezone_name)
		tonight = dt.datetime.combine(local_time.date(), dt.time(23,0))
		if local_time.hour >= 12:
			tomorrow_night = tonight + pd.Timedelta(days=1)
			end = pd.Timestamp(tomorrow_night).tz_localize(self.timezone_name)
		else:
			end = pd.Timestamp(tonight).tz_localize(self.timezone_name)
		return start, end
	def get_bidding_zones(self, start, end):
		# Austria split from the bidding zone on Oct. 1, 2018: UTC+2
		split_date = pd.Timestamp('20181001', tz=self.timezone_name)
		if start < split_date and end >= split_date:
			return [
				('DE-AT-LU', start, split_date),
				('DE-LU', split_date, end)
			]
		elif start < split_date and end < split_date:
			return [('DE-AT-LU', start, end)]
		elif start >= split_date and end >= split_date:
			return [('DE-LU', start, end)]