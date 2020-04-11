import numpy as np
import pandas as pd
import warnings
import sys

import datetime as dt

from .utils import group_contiguous_points

def simple_impute(df, col, verbose=True):
	imputed_df = df.copy(deep=True)
	for time in np.unique(df.index.time):
		if verbose:
			print("Imputation for time {}:".format(time))
		df_at_time = imputed_df[imputed_df.index.time == time]
		missing_values_index_at_time = np.unique(df_at_time[df_at_time[col].isnull()].index.date).tolist()
		print(missing_values_index_at_time)
		for start, end in group_contiguous_points(missing_values_index_at_time):
			start_time = dt.datetime.combine(start, time)
			end_time = dt.datetime.combine(end, time)
			try:
				prev_date_value = df_at_time.loc[start_time + dt.timedelta(-1), col]
			except KeyError as e:
				if verbose:
					print("Data at beginning skipped and date entry removed: {}-{}".format(start, end))
				imputed_df.drop(imputed_df.loc[:end].index, inplace=True)
				continue
			try:
				next_date_value = df_at_time.loc[end_time + dt.timedelta(1), col]
			except KeyError as e:
				if verbose:
					print("Data at end skipped: {}-{}".format(start, end))
				imputed_df.drop(imputed_df.loc[start:].index, inplace=True)
				continue
			# linear fitting
			number_of_days = (end - start).days + 1
			grad = (next_date_value - prev_date_value) / (number_of_days + 1)
			imputation_list = [prev_date_value + (grad * i) for i in range(1, number_of_days+1)]
			# impute the values
			for i in range(number_of_days):
				if verbose:
					print("{} imputed".format(start_time + dt.timedelta(i)))
				imputed_df.loc[start_time + dt.timedelta(i), col] = imputation_list[i]
	assert np.all(imputed_df[col].notnull()) == True
	return imputed_df