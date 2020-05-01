import pytest
import datetime as dt

import numpy as np
import pandas as pd

import tables

from empredictor.daily_dataframe import daily_dataframe
from empredictor.exceptions import InvalidTimeSlots, MoreThanOneContiguousDatapoint
from empredictor.bidding_zone_info import Germany

class Test_daily_dataframe:
	def test_daily_dataframe_instantiates_for_correct_dataframe(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,1,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,2,1,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,1,0), 
			]
		)
		daily_dataframe(test_df, Germany, [dt.time(0,0), dt.time(1,0)])

	def test_daily_dataframe_instantiates_for_correct_dataframe(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,1,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,2,1,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,1,0), 
			]
		)
		german_info = Germany()
		ddf = daily_dataframe(test_df, german_info, [dt.time(0,0), dt.time(1,0)])
		assert ddf.start == dt.date(2020,1,1)
		assert ddf.end == dt.date(2020,1,3)

	def test_daily_dataframe_fixes_DST_for_real_dataset_with_local_DST_included_time(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)

		assert ddf.start == dt.date(2015,1,1)
		assert ddf.end == dt.date(2020,2,6)

	def test_daily_dataframe_fix_DST_adds_nan_values_for_March_where_there_is_a_missing_hour(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)

		assert str(ddf.dataframe.loc[dt.datetime(2015, 3, 29, 2, 0), 'Day Ahead Price']) == 'nan'
		assert str(ddf.dataframe.loc[dt.datetime(2016, 3, 27, 2, 0), 'Day Ahead Price']) == 'nan'
		assert str(ddf.dataframe.loc[dt.datetime(2017, 3, 26, 2, 0), 'Day Ahead Price']) == 'nan'
		assert str(ddf.dataframe.loc[dt.datetime(2018, 3, 25, 2, 0), 'Day Ahead Price']) == 'nan'
		assert str(ddf.dataframe.loc[dt.datetime(2019, 3, 31, 2, 0), 'Day Ahead Price']) == 'nan'

	def test_daily_dataframe_fix_DST_does_not_add_nan_values_outside_of_dataframe_range(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)

		with pytest.raises(KeyError):
			ddf.dataframe.loc[dt.datetime(2020, 3, 29, 2, 0), 'Day Ahead Price']

	def test_daily_dataframe_fix_DST_deletes_duplicate_values_for_October(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)

		assert len(test_df.loc[dt.datetime(2015, 10, 25, 2, 0)]) == 2
		assert len(test_df.loc[dt.datetime(2016, 10, 30, 2, 0)]) == 2
		assert len(test_df.loc[dt.datetime(2017, 10, 29, 2, 0)]) == 2
		assert len(test_df.loc[dt.datetime(2018, 10, 28, 2, 0)]) == 2
		assert len(test_df.loc[dt.datetime(2019, 10, 27, 2, 0)]) == 2
		assert ddf.dataframe.loc[dt.datetime(2015, 10, 25, 2, 0), 'Day Ahead Price'] == 25.07
		assert ddf.dataframe.loc[dt.datetime(2016, 10, 30, 2, 0), 'Day Ahead Price'] == 31.55
		assert ddf.dataframe.loc[dt.datetime(2017, 10, 29, 2, 0), 'Day Ahead Price'] == -83.06
		assert ddf.dataframe.loc[dt.datetime(2018, 10, 28, 2, 0), 'Day Ahead Price'] == 41.62
		assert ddf.dataframe.loc[dt.datetime(2019, 10, 27, 2, 0), 'Day Ahead Price'] == -29.97

	def test_daily_dataframe_retrieves_correct_dates(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)

		date_index = ddf.datetimes()
		assert min(date_index) == pd.Timestamp('20150101 00:00:0000', tz="Europe/Berlin")
		assert max(date_index) == pd.Timestamp('20200206 23:00:0000', tz="Europe/Berlin")
		assert np.all(
			date_index == pd.date_range(
				start='20150101 00:00:0000',
				end='20200206 23:00:0000', 
				freq='H', 
				tz="Europe/Berlin"
			)
		)

	def test_daily_dataframe_initialises_correctly_from_ml_ready_df(self):
		test_df = pd.read_hdf('tests/test_data/ml_ready.hdf', key='da_prices')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_ml_ready_df(test_df, german_info, time_slots)

		assert ddf.start == dt.date(2015,1,6)
		assert ddf.end == dt.date(2020,4,29)

	def test_daily_dataframe_retrieves_correct_dates_for_end_of_DST_where_there_are_duplicates(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)
		assert len(ddf.retrieve(
			pd.Timestamp('20151025 00:00:0000', tz="Europe/Berlin"),
			pd.Timestamp('20151025 23:00:0000', tz="Europe/Berlin"),
			['Day Ahead Price']
		)) == 25
		assert len(ddf.retrieve(
			pd.Timestamp('20151025 02:00:0000+02:00', tz="Europe/Berlin"),
			pd.Timestamp('20151025 02:00:0000+01:00', tz="Europe/Berlin"),
			['Day Ahead Price']
		)) == 2

	def test_daily_dataframe_retrieves_only_23_times_for_beginning_of_DST(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)
		assert len(ddf.retrieve(
			pd.Timestamp('20150329 00:00:0000', tz="Europe/Berlin"),
			pd.Timestamp('20150329 23:00:0000', tz="Europe/Berlin"),
			['Day Ahead Price']
		)) == 23

	def test_daily_dataframe_verification_works_for_correct_dataframe(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,1,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,2,1,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,1,0), 
			]
		)
		assert daily_dataframe.verify_data_integrity(test_df, [dt.time(0,0), dt.time(1,0)]) == (
			dt.date(2020,1,1), 
			dt.date(2020,1,3), 
		)

	def test_daily_dataframe_verification_raises_error_for_dates_with_missing_timeslots(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,1,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,1,0), 
			]
		)
		with pytest.raises(InvalidTimeSlots) as e:
			daily_dataframe.verify_data_integrity(test_df, [dt.time(0,0), dt.time(1,0)])
		error_message = str(e.value)
		assert 'datetime.date(2020, 1, 2)' in error_message

	def test_daily_dataframe_verification_raises_error_for_dates_with_repeating_timeslots(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,1,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,2,1,0), 
				dt.datetime(2020,1,2,1,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,1,0), 
			]
		)
		with pytest.raises(InvalidTimeSlots) as e:
			daily_dataframe.verify_data_integrity(test_df, [dt.time(0,0), dt.time(1,0)])
		error_message = str(e.value)
		assert 'datetime.date(2020, 1, 2)' in error_message

	def test_daily_dataframe_verification_raises_error_for_real_dataset_with_local_DST_included_time(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		test_df.set_index(test_df.index.tz_localize(None), inplace=True)
		time_slots = [dt.time(i,0) for i in range(24)]
		with pytest.raises(InvalidTimeSlots) as e:
			daily_dataframe.verify_data_integrity(test_df, time_slots)
		error_message = str(e.value)
		assert 'datetime.date(2015, 3, 29)' in error_message
		assert 'datetime.date(2015, 10, 25)' in error_message
		assert 'datetime.date(2016, 3, 27)' in error_message
		assert 'datetime.date(2016, 10, 30)' in error_message
		assert 'datetime.date(2017, 3, 26)' in error_message
		assert 'datetime.date(2017, 10, 29)' in error_message
		assert 'datetime.date(2018, 3, 25)' in error_message
		assert 'datetime.date(2018, 10, 28)' in error_message
		assert 'datetime.date(2019, 3, 31)' in error_message
		assert 'datetime.date(2019, 10, 27)' in error_message

	def test_daily_dataframe_raises_error_for_non_contiguous_dates(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,2,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,2,0), 
			]
		)
		with pytest.raises(MoreThanOneContiguousDatapoint) as e:
			daily_dataframe.verify_data_integrity(test_df, [dt.time(0,0), dt.time(2,0)])
		error_message = str(e.value)
		assert '(datetime.date(2020, 1, 1), datetime.date(2020, 1, 1))' in error_message
		assert '(datetime.date(2020, 1, 3), datetime.date(2020, 1, 3))' in error_message

	def test_daily_dataframe_len_works_as_expected(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,1,2,0), 
				dt.datetime(2020,1,2,0,0), 
				dt.datetime(2020,1,2,2,0), 
			]
		)
		german_info = Germany()
		ddf = daily_dataframe.from_ml_ready_df(test_df, german_info, [dt.time(0,0), dt.time(2,0)])

		assert len(ddf) == 4
		
	def test_daily_dataframe_indexing_works_as_expected(self):
		test_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='raw_df')
		german_info = Germany()
		time_slots = [dt.time(i,0) for i in range(24)]

		ddf = daily_dataframe.from_tz_aware_df(test_df, german_info, time_slots)
		start = pd.Timestamp('20151025 00:00:0000', tz="Europe/Berlin")
		end = pd.Timestamp('20151025 23:00:0000', tz="Europe/Berlin")
		print(ddf[start:end])
		assert False