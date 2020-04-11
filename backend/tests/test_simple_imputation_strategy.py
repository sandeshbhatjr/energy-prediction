import pytest
import datetime as dt

import numpy as np
import pandas as pd

from empredictor.imputation_strategy import simple_impute

def test_simple_imputation_removes_missing_beginning_values():
	test_df = pd.DataFrame(
		data=[
			{'v': np.nan}, 
			{'v': 1}, 
			{'v': 1}, 
		], 
		index=[
			dt.datetime(2020,1,1), 
			dt.datetime(2020,1,2), 
			dt.datetime(2020,1,3), 
		]
	)
	imputed_df = simple_impute(test_df, 'v', verbose=True)
	with pytest.raises(KeyError):
		imputed_df.loc[dt.datetime(2020,1,1), 'v']
	assert imputed_df.loc[dt.datetime(2020,1,2), 'v'] == 1
	assert imputed_df.loc[dt.datetime(2020,1,3), 'v'] == 1

def test_simple_imputation_removes_missing_end_values():
	test_df = pd.DataFrame(
		data=[
			{'v': 1}, 
			{'v': 1}, 
			{'v': np.nan}, 
		], 
		index=[
			dt.datetime(2020,1,1,0,0), 
			dt.datetime(2020,1,2,0,0), 
			dt.datetime(2020,1,3,0,0), 
		]
	)
	imputed_df = simple_impute(test_df, 'v', verbose=True)
	with pytest.raises(KeyError):
		imputed_df.loc[dt.datetime(2020,1,3), 'v']
	assert imputed_df.loc[dt.datetime(2020,1,1), 'v'] == 1
	assert imputed_df.loc[dt.datetime(2020,1,2), 'v'] == 1

def test_simple_imputation_works_for_missing_intermediate_values():
	test_df = pd.DataFrame(
		data=[
			{'v': 1}, 
			{'v': np.nan}, 
			{'v': 1},
		], 
		index=[
			dt.datetime(2020,1,1), 
			dt.datetime(2020,1,2), 
			dt.datetime(2020,1,3),
		]
	)
	imputed_df = simple_impute(test_df, 'v', verbose=True)
	assert imputed_df.loc[dt.datetime(2020,1,2), 'v'] == 1