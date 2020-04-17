import numpy as np
import pandas as pd
import datetime as dt

import time

from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError
from requests import HTTPError

from .utils import when_is_DST, group_contiguous_points
from .exceptions import RequestFailure, IncorrectAPIKey

# coding very defensively here
class daily_dataframe:
	def __init__(self, dataframe, offset_from_UTC=0):
		self.offset_from_UTC = offset_from_UTC
		if self.verify_data_integrity(dataframe):
			self.dataframe = dataframe
		# what to do with incorrect dataframe?
		# CASE 1: Only few dates with a timeslot- remove the timeslot
		# CASE 2: Non-contigious date-points: take the largest one?
		# Or add in in-between dates if it is < threshold
		# CASE 3: A few missing times for some dates- replace with nan
	def retrieve(self, dates):
		# retrieves entries from tz-aware dates
		pass
	def in_multivariate_form(self):
		pass
	def get_windowed_dataset(self, X_cols, y_cols, window_size, **kwargs):
		try:
			batch_size = kwargs['batch_size']
		except KeyError:
			batch_size = len(self.dataframe.index)
	def dates(self, in_timezone=False):
		if in_timezone:
			# first, remove offset and convert to UTC
			UTC_datetime_index = self.dataframe.index - pd.Timedelta(hours=self.offset_from_UTC)
			# localise
			local_datetime_index = UTC_datetime_index.tz_localize('utc').tz_convert(in_timezone)
			return local_datetime_index
		else:
			return self.dataframe.index
	@staticmethod
	def compare(new_ddf, old_ddf):
		return list(set(new_ddf.dates()) - set(old_ddf.dates()))
	@staticmethod
	def verify_data_integrity(dataframe):
		# check all columns are as expected
		# 1: check each day has the same set of timeslots
		unique_times, counts = np.unique(dataframe.index.time, return_counts=True)
		contigious_dates = {
			time: group_contiguous_points(dataframe[dataframe.index.time == time].index.tolist()) for time in unique_times
		}
		return True

class da_price:
	"""Day ahead price of electricity dataset in the DE-LU bidding zone, post 2015."""
	def __init__(self, API_key, country_info, cache_filename='cache.hdf', verbose=True, **kwargs):
		self.cache_filename = cache_filename
		self.API_key = API_key
		self.verbose = verbose
		self.country_info = country_info()
		self.load_cache()
		self.update()
		# save to cache for further use
		self.save_to_cache()
	def __del__(self):
		self.save_to_cache()
	def load_cache(self):
		try:
			# load from cache
			df = pd.read_hdf(self.cache_filename, key='da_prices')
			self.cache_ddf = daily_dataframe(df, offset_from_UTC=self.country_info.hour_offset_to_UTC)
			self.current_ddf = daily_dataframe(df.copy(deep=True), offset_from_UTC=self.country_info.hour_offset_to_UTC)
		except FileNotFoundError:
			if self.verbose:
				print('Cache not found: Creating one at {}.'.format(self.cache_filename))
			# retrieve the whole dataset from entsoe and save it to cache
			start, end = self.country_info.get_range()
			df = self.from_entsoe(start, end)
			self.cache_ddf = daily_dataframe(df, offset_from_UTC=self.country_info.hour_offset_to_UTC)
			self.current_ddf = daily_dataframe(df.copy(deep=True), offset_from_UTC=self.country_info.hour_offset_to_UTC)
		# update: this will not do anything if the cache was empty, and the exception was triggered
	def save_to_cache(self):
		# make sure the dataframe is in the right format
		dates_to_add = daily_dataframe.compare(self.current_ddf, self.cache_ddf)
		if dates_to_add != []:
			df_to_save = pd.concat([self.cache_ddf.dataframe, self.current_ddf.dataframe.loc[dates_to_add]])
			df_to_save.to_hdf(self.cache_filename, key='da_prices')
			if self.verbose:
				print('Cache saved; {} updated.'.format(dates_to_add))
	def update(self):
		start = max(self.cache_ddf.dates(in_timezone=self.country_info.timezone_name))
		_, end = self.country_info.get_range()
		if end > start:
			if self.verbose:
				print("Updating entries from {} till {}".format(start, end))
			self.from_entsoe(start, end)
		else:
			print('Cache up-to-date')
	def get(self, starting_from, until, thorough=False):
		# check if dates are within range
		start, end = self.country_info.get_range()
		if starting_from < start or until > end:
			print('{}-{} out of bounds for Germany'.format(starting_from, until))
			return None
		try:
			return self.current_ddf.dataframe.loc[starting_from:until, 'Day Ahead Price']
		except KeyError:
			print("Entry not found: Reloading cache")
			# reload cache, since maybe it was updated by another service
			self.load_cache()
		# try again
		try:
			return self.current_ddf.dataframe.loc[starting_from:until, 'Day Ahead Price']
		except KeyError:
			# update cache
			print("Entry still not found: Attempting cache update")
			self.update()
			return self.current_ddf.dataframe.loc[starting_from:until, 'Day Ahead Price']
			self.save_to_cache()
	def from_entsoe(self, starting, until):
		"""
			Retrieve day-ahead price from entsoe using their API.
			Needs API key.
		"""
		df = pd.DataFrame(columns=['Day Ahead Price'])
		bidding_zones = self.country_info.get_bidding_zones(starting, until)
		for bidding_zone, start, end in bidding_zones:
			client = EntsoePandasClient(api_key=self.API_key)
			try:
				df_to_append = client.query_day_ahead_prices(bidding_zone, start=start, end=end).to_frame('Day Ahead Price')
			except NoMatchingDataError as e:
				if self.verbose:
					print(e)
				return None
			except HTTPError as e:
				if e.response.status_code == 429:
					if self.verbose:
						print('Too many requests: waiting for 360 seconds before retrying')
					time.sleep(360)
					# retry once
					df_to_append = client.query_day_ahead_prices(bidding_zone, start=start, end=end).to_frame('Day Ahead Price')
					# raise RequestFailure({'reason': 'Too many requests'})
				if e.response.status_code == 401:
					raise IncorrectAPIKey('The API key is incorrect')
			except Exception as e:
				raise e
			UTC_datetime_index = df_to_append.index.tz_convert(None)
			# convert datetime index to UTC + offset
			physical_datetime_index = UTC_datetime_index + pd.to_timedelta(self.country_info.hour_offset_to_UTC, unit='h')
			df_to_append.set_index(physical_datetime_index, inplace=True)
			# append to full dataframe
			df = pd.concat([df, df_to_append])
		return df
