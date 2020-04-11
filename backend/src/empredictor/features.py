import pandas as pd
from holidays import Germany, Austria, Luxembourg

from .utils import when_is_DST

# ALL THESE FUNCTIONS WORK ONLY WHEN THE INDEX OF THE PASSED DATAFRAME IS A DATETIME OBJECT

# weekday
def weekday_feature(df):
	return df.index.weekday

# holidays
def holiday_features(df, ohe=False):
	german_holidays = sum([Germany(prov=x) for x in Germany.PROVINCES])
	austrian_holidays = sum([Austria(prov=x) for x in Austria.PROVINCES])
	luxembourg_holidays = Luxembourg()

	all_holidays = german_holidays + austrian_holidays + luxembourg_holidays

	def get_holiday(date):
		try:
			day_type = all_holidays[date]
		except KeyError:
			day_type = 'None'
		return day_type

	return df.index.map(lambda x: get_holiday(x))


# DST or not?
def DST(df):
	pass

# STL decomposition?
def STL(df):
	pass