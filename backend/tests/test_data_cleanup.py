import pytest
import datetime as dt
import os

import pandas as pd

from empredictor.data_cleanup import da_price
from empredictor.exceptions import IncorrectAPIKey
from empredictor.bidding_zone_info import Germany

from entsoe import EntsoePandasClient

def mockPandasTimestampNow(tz=None):
	return pd.Timestamp('20150109 04:00:0000', tz=tz)
	
def mock_EntsoePandasClientQueryDayAheadPrice(self, bidding_zone, start=pd.Timestamp('20150101', tz='Europe/Berlin'), end=pd.Timestamp('20150110', tz='Europe/Berlin')):
	fake_df = pd.read_hdf('tests/test_data/manually_processed_dataframes', key='from_entsoe')
	return fake_df

class Test_da_price:
	# TODO: LOT MORE TESTS NEEDED HERE!!! And the tech debt rises...
	def test_da_price_loads_cache_when_cache_file_exists(self, monkeypatch):
		# da_price_germany = da_price('key', Germany, cache_filename='tests/test_data/cache.hdf')
		pass
	def test_da_price_raises_error_when_cache_is_corrupt(self):
		pass
	def test_da_price_retrieves_correct_entries_from_entsoe(self, monkeypatch):
		monkeypatch.setattr(EntsoePandasClient, 'query_day_ahead_prices', mock_EntsoePandasClientQueryDayAheadPrice)
		monkeypatch.setattr(pd.Timestamp, 'now', mockPandasTimestampNow)
		da_price_germany = da_price('key', Germany, cache_filename='tests/test_data/temp_cache.hdf')

		# TODO: Write a proper test
		print(da_price_germany.ddf.dataframe)
		# cleanup
		os.remove('tests/test_data/temp_cache.hdf')

	def test_da_price_from_entsoe_works(self):
		# da_price_germany = da_price('key', Germany, cache_filename='tests/test_data/cache.hdf')
		# unique, counts = np.unique(da_price_germany.cache_ddf.dataframe.index.date, return_counts=True)
		# print(unique[counts != 24])
		pass
		# cleanup
		# os.remove('tests/test_data/cache.hdf')
	def test_da_prices_raises_custom_exception_for_incorrect_API_key(self):
		pass
		# mock request here! SHOULD NOT USE THE API
		# with pytest.raises(IncorrectAPIKey):
		# 	da_price_germany = da_price('incorrect-api-key', Germany, cache_filename='tests/test_data/nonexistent-cache.hdf')
	