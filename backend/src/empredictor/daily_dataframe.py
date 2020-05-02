import numpy as np
import pandas as pd
import datetime as dt

from .utils import group_contiguous_points

from .exceptions import (
	InvalidTimeSlots, 
	MoreThanOneContiguousDatapoint
)

# coding very defensively here
# this enables one to work with datasets where 
# a fixed number of entries (for e.g, hourly) are provided for each day
class daily_dataframe:
	def __init__(self, dataframe, country, timeslots):
		"""
			Initialize with dataframe in ml-ready format with fixed number of timeslots per day.
			When there is DST, there are two days in a year when there are repeated/deleted hours.
			If your dataframe is in a local timezone with DST, use from_tz_aware_df() class method.
			If your dataframe is already processed into a ML ready format, use from_ml_ready_df().
		"""
		self.start, self.end = self.verify_data_integrity(dataframe, timeslots)
		self.dataframe = dataframe
		self.country = country
		self.timeslots = timeslots
		self.duplicate_datetimes_removed, self.fake_datetimes_added = self \
				.get_DST_duplicate_and_missing_times(self.start, self.end, self.country, self.timeslots)
		# TODO: Attempt to fix when there are a few missing timeslots- replace with nan?
	@classmethod
	def from_ml_ready_df(cls, dataframe, country, timeslots):
		start, end = cls.verify_data_integrity(dataframe, timeslots)
		return cls(dataframe, country, timeslots)
	@classmethod
	def from_tz_aware_df(cls, dataframe, country, timeslots):
		# convert datetime index to country_info timezone
		local_datetime_index = dataframe.index.tz_convert(country.timezone_name).tz_localize(None)
		local_dataframe = dataframe.set_index(local_datetime_index)
		# convert to ML ready form
		# Note that this leads to the repeated data at the end of DST to be lost forever!
		start = min(local_datetime_index.date)
		end = max(local_datetime_index.date)
		datetimes_with_duplicates, fake_datetimes_to_add = cls \
			.get_DST_duplicate_and_missing_times(start, end, country, timeslots)
		columns = sorted(local_dataframe)
		fake_dict = {
			column: {
				fake_datetime_to_add: np.nan for fake_datetime_to_add in fake_datetimes_to_add
			} 
			for column in columns
		}
		# combine them
		rest_of_dataframe = local_dataframe.drop(datetimes_with_duplicates)
		fake_df = pd.DataFrame(fake_dict)
		dataframe_with_duplicates = local_dataframe.loc[datetimes_with_duplicates]
		dataframe_with_duplicates_removed = dataframe_with_duplicates \
			.loc[~dataframe_with_duplicates.index.duplicated(keep='first')]
		DST_corrected_dataframe = (
			pd.concat([fake_df, dataframe_with_duplicates_removed, rest_of_dataframe])
		).sort_index()
		return cls(DST_corrected_dataframe, country, timeslots)
	def __len__(self):
		return len(self.dataframe)
	def datetimes(self, return_range=False):
		"""
			Returns datetime index as tz-aware datetimes.
		"""
		local_datetime_list = sorted(
			list(set(self.dataframe.index) - set(self.fake_datetimes_added)) + 
			(self.duplicate_datetimes_removed)
		)
		local_datetime_index = pd.Index(local_datetime_list)
		tz_aware_datetime_index = local_datetime_index.tz_localize(self.country.timezone_name, ambiguous='infer')
		if return_range:
			return min(tz_aware_datetime_index), max(tz_aware_datetime_index)
		else:
			return tz_aware_datetime_index
	def retrieve(self, start, end, column_names):
		"""
			Retrieves entries using tz-aware dates.
			Follows the pandas convention: the entries are inclusive of start and end
		"""
		local_start, local_end = (
			start.tz_convert(self.country.timezone_name).tz_localize(None), 
			end.tz_convert(self.country.timezone_name).tz_localize(None)
		)
		# deal with removed duplicate values
		datetimes_with_duplicates, fake_datetimes_added = self \
			.get_DST_duplicate_and_missing_times(local_start, local_end, self.country, self.timeslots)
		rest_of_df = self.dataframe.loc[local_start:local_end, column_names]
		nan_for_duplicates = {
			column: {
				datetime_with_duplicate: np.nan for datetime_with_duplicate in datetimes_with_duplicates
			} 
			for column in column_names
		}
		duplicate_df = pd.DataFrame(nan_for_duplicates)
		local_df = (
			pd.concat([duplicate_df, rest_of_df.drop(fake_datetimes_added)])
		).sort_index()
		tz_aware_df = local_df.tz_localize(self.country.timezone_name, ambiguous='infer')
		return tz_aware_df
	@staticmethod
	def compare(new_ddf, old_ddf):
		"""
			Returns all tz-aware dates in new_ddf, but not in old_ddf, as a list.
		"""
		return list(set(new_ddf.datetimes()) - set(old_ddf.datetimes()))
	@classmethod
	def append(cls, ddf, ddf_to_append):
		"""
			Appends ddf_to_append to ddf, sorts it and return the appended ddf.
			For this to work, the appended ddf should still satisfy the contiguous and timeslot condition.
		"""
		assert ddf.country == ddf_to_append.country
		assert ddf.timeslots == ddf_to_append.timeslots
		return cls(pd.concat([ddf.dataframe, ddf_to_append.dataframe]), ddf.country, ddf.timeslots)
	@staticmethod
	def verify_data_integrity(dataframe, timeslots):
		"""
			Checks if the index consists of a fixed time slots per day in one contiguous unit across days.
			Index should be tz-naive datetime objects.
		"""
		timeslots_by_day = { 
			key.date(): value.time for key, value in dataframe.index.groupby(dataframe.index.date).items()
		}
		# gather dates with incorrect time slots
		incorrect_dates = {
			day: timeslots_of_day 
			for day, timeslots_of_day in timeslots_by_day.items() 
			if not (sorted(timeslots_of_day) == sorted(timeslots)) 
		}
		if len(incorrect_dates) is not 0:
			raise InvalidTimeSlots('Invalid Timeslots on {}'.format(list(incorrect_dates.keys())), incorrect_dates)
		unique_dates = np.unique(dataframe.index.date)
		contiguous_dates = group_contiguous_points(unique_dates)
		if len(contiguous_dates) is not 1:
			raise MoreThanOneContiguousDatapoint(
				'Dates split into multiple contiguous units: {}'.format(contiguous_dates), 
				contiguous_dates
			)
		else:
			return contiguous_dates[0]
	@staticmethod
	def get_DST_duplicate_and_missing_times(start, end, country, timeslots):
		# Assume the dataset is contiguous in dates
		datetimes_to_add, datetimes_to_remove = country.get_DST_datetime(start, end)
		non_existent_rows, rows_with_duplicates = [], []
		# At the end of DST, the time shifts back by an hour, causing duplicate time for an hour
		for datetime_to_remove in datetimes_to_remove:
			relevant_timeslots = list(filter(
				lambda x: 
					(x >= datetime_to_remove.time()) and 
					(x < (datetime_to_remove + dt.timedelta(hours=1)).time()), 
				timeslots
			))
			rows_with_duplicates += [
				dt.datetime.combine(datetime_to_remove.date(), timeslot) 
				for timeslot in relevant_timeslots
			]
		# At the beginning of DST, the time shifts forward by an hour, causing a missing hour
		for datetime_to_add in datetimes_to_add:
			relevant_timeslots = list(filter(
				lambda x: 
					(x >= (datetime_to_add - dt.timedelta(hours=1)).time()) and 
					(x < datetime_to_add.time()), 
				timeslots
			))
			non_existent_rows += [
				dt.datetime.combine(datetime_to_add.date(), timeslot) for timeslot in relevant_timeslots
			]
		return rows_with_duplicates, non_existent_rows
