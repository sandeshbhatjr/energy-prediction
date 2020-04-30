import pandas as pd
import pytz
import pytest
import datetime as dt

from empredictor.bidding_zone_info import Germany

class Test_Germany:
	def test_local_info_for_Germany_is_correct(self):
		german_local_data = Germany()
		assert german_local_data.timezone_name == 'Europe/Berlin'
		assert german_local_data.hour_offset_to_UTC == 1

	def test_date_range_for_Germany_is_timezone_aware(self):
		german_local_data = Germany()
		start, end = german_local_data.get_range()
		assert start.tzname() == 'CET'
		assert end.tzname() == 'CEST'

	def test_get_zones_for_Germany_for_dates_before_and_after_split(self):
		start = pd.Timestamp('20151201', tz='Europe/Berlin')
		end = pd.Timestamp('20181001', tz='Europe/Berlin')
		german_local_data = Germany()
		bidding_zones = german_local_data.get_bidding_zones(start, end)
		assert bidding_zones == [
			('DE-AT-LU', pd.Timestamp('20151201', tz='Europe/Berlin'), pd.Timestamp('20181001', tz='Europe/Berlin')),
			('DE-LU', pd.Timestamp('20181001', tz='Europe/Berlin'), pd.Timestamp('20181001', tz='Europe/Berlin'))
		]

	def test_get_zones_for_Germany_for_dates_before_split(self):
		start = pd.Timestamp('20151201', tz='Europe/Berlin')
		end = pd.Timestamp('20180930', tz='Europe/Berlin')
		german_local_data = Germany()
		bidding_zones = german_local_data.get_bidding_zones(start, end)
		assert bidding_zones == [
			('DE-AT-LU', pd.Timestamp('20151201', tz='Europe/Berlin'), pd.Timestamp('20180930', tz='Europe/Berlin'))
		]

	def test_get_zones_for_Germany_for_dates_after_split(self):
		start = pd.Timestamp('20181001', tz='Europe/Berlin')
		end = pd.Timestamp('20190930', tz='Europe/Berlin')
		german_local_data = Germany()
		bidding_zones = german_local_data.get_bidding_zones(start, end)
		assert bidding_zones == [
			('DE-LU', pd.Timestamp('20181001', tz='Europe/Berlin'), pd.Timestamp('20190930', tz='Europe/Berlin'))
		]

	def test_bidding_zones_returned_are_accurate_from_01_2015_to_12_2015(self):
		start = dt.date(2015, 1, 1)
		end = dt.date(2015, 12, 1)
		german_local_data = Germany()
		assert german_local_data.get_DST_datetime(start, end) == (
			[dt.datetime(2015, 3, 29, 3, 0)], 
			[dt.datetime(2015, 10, 25, 2, 0)]
		)

	def test_bidding_zones_returned_are_empty_when_non_DST_datetime_ranges_are_considered(self):
		start = dt.date(2015, 1, 1)
		end = dt.date(2015, 2, 1)
		german_local_data = Germany()
		assert german_local_data.get_DST_datetime(start, end) == (
			[], 
			[]
		)

	def test_bidding_zones_returned_are_accurate_when_only_half_a_year_after_start_of_DST_is_considered(self):
		start = dt.date(2015, 4, 1)
		end = dt.date(2015, 12, 1)
		german_local_data = Germany()
		assert german_local_data.get_DST_datetime(start, end) == (
			[], 
			[dt.datetime(2015, 10, 25, 2, 0)]
		)

	def test_bidding_zones_returned_are_accurate_when_only_half_a_year_before_end_of_DST_is_considered(self):
		start = dt.date(2015, 1, 1)
		end = dt.date(2015, 8, 1)
		german_local_data = Germany()
		assert german_local_data.get_DST_datetime(start, end) == (
			[dt.datetime(2015, 3, 29, 3, 0)], 
			[]
		)
