import pandas as pd
import pytz
import pytest

from empredictor.bidding_zone_info import Germany

class Test_Germany:
	def test_local_info_for_Germany_is_correct(self):
		german_local_data = Germany()
		assert german_local_data.timezone_name == 'Europe/Berlin'
		assert german_local_data.timezone == pytz.timezone('Europe/Berlin')
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