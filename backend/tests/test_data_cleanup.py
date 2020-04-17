import pytest
import datetime as dt
import os

import numpy as np
import pandas as pd

from empredictor.data_cleanup import daily_dataframe, da_price
from empredictor.exceptions import IncorrectAPIKey
from empredictor.bidding_zone_info import Germany

class Test_daily_dataframe:
	def test_daily_dataframe_instantiates(self):
		pass
	def test_daily_dataframe_correct_date_time_index_with_uneven_daily_periods(self):
		test_df = pd.DataFrame(
			data=[
				{'v': 1}, 
				{'v': 1}, 
				{'v': 1}, 
			], 
			index=[
				dt.datetime(2020,1,1,0,0), 
				dt.datetime(2020,1,2,2,0), 
				dt.datetime(2020,1,3,0,0), 
			]
		)
		# assert daily_dataframe.verify_data_integrity(test_df) == False, (dt.datetime(2020,1,2,2,0))
	def test_daily_dataframe_works_for_split_dates(self):
		pass
	def test_daily_dataframe_rejects_ddf_with_missing_hours_for_some_dates(self):
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
				dt.datetime(2020,1,1,2,0), 
				dt.datetime(2020,1,2,2,0), 
				dt.datetime(2020,1,2,2,0), 
				dt.datetime(2020,1,3,0,0), 
				dt.datetime(2020,1,3,2,0), 
			]
		)
		# assert daily_dataframe.verify_data_integrity(test_df) == False, (dt.datetime(2020,1,2,2,0), dt.datetime(2020,1,2,2,0))

class Test_da_price:
	# TODO: LOT MORE TESTS NEEDED HERE!!! And the tech debt rises...
	def test_da_price_loads_cache_when_cache_file_exists(self):
		# da_price_germany = da_price('key', Germany, cache_filename='tests/test_data/cache.hdf')
		pass
	def test_da_price_from_entsoe_works(self):
		# da_price_germany = da_price('key', Germany, cache_filename='tests/test_data/cache.hdf')
		# unique, counts = np.unique(da_price_germany.cache_ddf.dataframe.index.date, return_counts=True)
		# print(unique[counts != 24])
		pass
		# cleanup
		# os.remove('tests/test_data/cache.hdf')
	def test_da_prices_raises_custom_exception_for_incorrect_API_key(self):
		# mock request here! SHOULD NOT USE THE API
		with pytest.raises(IncorrectAPIKey):
			da_price_germany = da_price('incorrect-api-key', Germany, cache_filename='tests/test_data/nonexistent-cache.hdf')
	