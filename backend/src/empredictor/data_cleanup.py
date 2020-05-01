import numpy as np
import pandas as pd
import datetime as dt

import time
import tables

from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError
from requests import HTTPError

from .daily_dataframe import daily_dataframe
from .utils import group_contiguous_points
from .exceptions import (
	InvalidTimeSlots, 
	MoreThanOneContiguousDatapoint,
	RequestFailure, 
	IncorrectAPIKey
)

class da_price:
	"""Day ahead price of electricity dataset in the DE-LU bidding zone, post 2015."""
	def __init__(self, API_key, country_class, cache_filename='cache.hdf', verbose=True, **kwargs):
		self.cache_filename = cache_filename
		self.API_key = API_key
		self.verbose = verbose
		self.country = country_class()
		self.time_slots = [dt.time(i,0) for i in range(24)]
		self.ddf = self.load_data()
		self.update()
		# save to cache for further use
		self.save_to_cache()
	def __del__(self):
		try:
			self.save_to_cache()
		except FileNotFoundError:
			pass
	def load_data(self):
		try:
			# load from cache
			df = pd.read_hdf(self.cache_filename, key='da_prices')
			ddf = daily_dataframe.from_ml_ready_df(df, self.country, self.time_slots)
		except (FileNotFoundError, MoreThanOneContiguousDatapoint, InvalidTimeSlots):
			if self.verbose:
				print('Cache not found/corrupt: Creating one at {}.'.format(self.cache_filename))
			# retrieve the whole dataset from entsoe
			start, end = self.country.get_range()
			print("Fetching data from {} to {}".format(start, end))
			ddf = self.from_entsoe(start, end)
		return ddf
	def update(self):
		"""
			Updates the daily dataframe until date specified by the country_info date range.
			For example, for Germany, this is until end of tomorrow if after 12.00 PM.
		"""
		_, current_end = self.ddf.datetimes(return_range=True)
		start = current_end + pd.Timedelta(hours=1)
		_, end = self.country.get_range()
		if end > start:
			if self.verbose:
				print("Updating entries from {} until {}".format(start, end))
			try:
				ddf_to_update = self.from_entsoe(start, end)
				# append to full dataframe
				self.ddf = daily_dataframe.append(self.ddf, ddf_to_update)
			except NoMatchingDataError as e:
				print("Update did not succeed:")
				print(e)
		else:
			print('Cache up-to-date')
	def save_to_cache(self):
		""" 
			Saves additional entries for daily dataframe to cache.
		"""
		try:
			cache_df = pd.read_hdf(self.cache_filename, key='da_prices')
			cache_ddf = daily_dataframe.from_ml_ready_df(cache_df, self.country, self.time_slots)
			dates_to_add = daily_dataframe.compare(self.ddf, cache_ddf)
			if dates_to_add != []:
				update_dates_start, update_dates_end = (group_contiguous_points(dates_to_add))[0]
				df_to_update = self.ddf.dataframe.loc[update_dates_start, update_dates_end, 'Day Ahead Price']
				df_to_update.set_index(df_to_update.index.tz_localize(None), inplace=True)
				print(df_to_update)
				df_to_save = pd.concat([cache_ddf.dataframe, df_to_update])
				df_to_save.to_hdf(self.cache_filename, key='da_prices')
				if self.verbose:
					print('Cache saved; {} updated.'.format(dates_to_add))
		except FileNotFoundError:
			self.ddf.dataframe.to_hdf(self.cache_filename, key='da_prices')
	def get(self, starting_from, until, thorough=False):
		"""
			Retrieve day-ahead prices for the timezone-aware dates from starting_from to until.
			If entry not found, the cache is reloaded, and checked.
			If still not found, cache is updated, and then checked finally.
			If thorough is True, it additionally checks entsoe for the specific dates 
			if the key is not found in cache.
		"""
		# check if dates are within range
		start, end = self.country.get_range()
		if starting_from < start or until > end:
			print('{}-{} out of bounds for Germany'.format(starting_from, until))
			return None
		try:
			return self.ddf.retrieve(starting_from, until, ['Day Ahead Price'])
		except KeyError:
			print("Entry not found: Reloading cache")
			# reload cache, since maybe it was updated by another service
			self.load_data()
		# try again
		try:
			return self.ddf.retrieve(starting_from, until, 'Day Ahead Price')
		except KeyError:
			# update cache
			print("Entry still not found: Attempting cache update")
			self.update()
			return self.ddf.retrieve(starting_from, until, 'Day Ahead Price')
			self.save_to_cache()
		if thorough:
			temp_ddf = self.from_entsoe(starting_from, until)
			return temp_ddf.dataframe['Day Ahead Price']
	def from_entsoe(self, starting, until):
		"""
			Retrieve day-ahead price from entsoe using their API.
			Retrieved dates includes dates from 'starting' upto- but not including- 'until'.
			Needs API key.
		"""
		df = pd.DataFrame(columns=['Day Ahead Price'])
		bidding_zones = self.country.get_bidding_zones(starting, until)
		for bidding_zone, start, end in bidding_zones:
			client = EntsoePandasClient(api_key=self.API_key)
			try:
				df_to_append = client.query_day_ahead_prices(bidding_zone, start=start, end=end).to_frame('Day Ahead Price')
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
			# append to full dataframe
			df = pd.concat([df, df_to_append])
		ddf = daily_dataframe.from_tz_aware_df(df, self.country, self.time_slots)
		return ddf
