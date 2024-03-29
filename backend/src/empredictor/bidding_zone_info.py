import datetime as dt
import pandas as pd

from .utils import when_is_last_sunday_of_march_and_october

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
		if local_time.hour >= 15:
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
	def get_DST_datetime(self, start, end):
		"""
			start, end should be passed in local time
		"""
		list_of_DST_dates = [
			when_is_last_sunday_of_march_and_october(year) for year in range(start.year, end.year + 1)
		]
		list_of_DST_start_dates = [
			start_date for start_date, _ in list_of_DST_dates 
			if (start_date <= end) and (start_date >= start)
		]
		list_of_DST_start_datetimes = list(map(lambda date: dt.datetime.combine(date, dt.time(3,0)), list_of_DST_start_dates))
		list_of_DST_end_dates = [
			end_date for _, end_date in list_of_DST_dates 
			if (end_date <= end) and (end_date >= start)
		]
		list_of_DST_end_datetimes = list(map(lambda date: dt.datetime.combine(date, dt.time(2,0)), list_of_DST_end_dates))
		return list_of_DST_start_datetimes, list_of_DST_end_datetimes
