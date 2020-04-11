import pytest
import datetime as dt
from empredictor import utils

def test_when_is_DST():
	for year in range(2015, 2050):
		start, end = utils.when_is_DST(year)
		# it starts in March and ends in October
		assert start.month == 3
		assert end.month == 10
		# is on a Sunday
		assert start.weekday() == 6
		assert end.weekday() == 6
		# is it the last sunday?
		# => next sunday is in the next month
		start_next_sunday, end_next_sunday = start + dt.timedelta(days=7), end + dt.timedelta(days=7)
		assert start_next_sunday.month == 4
		assert end_next_sunday.month == 11


class Test_group_contiguous_points:
	def test_for_empty_list(self):
		assert utils.group_contiguous_points([]) == []

	def test_for_a_single_date(self):
		test_date = dt.date(2030,1,1)
		assert utils.group_contiguous_points([test_date]) == [(test_date, test_date)]

	def test_for_multiple_dates(self):
		test_dates = [dt.date(2030,1,1), dt.date(2030,1,2), dt.date(2030,1,3), dt.date(2030,1,5), dt.date(2030,1,6)]
		assert utils.group_contiguous_points(test_dates) == [
			(dt.date(2030,1,1), dt.date(2030,1,3)),
			(dt.date(2030,1,5), dt.date(2030,1,6))
		]

	def test_for_unsorted_dates(self):
		test_dates = [dt.date(2030,1,2), dt.date(2030,1,1), dt.date(2030,1,3), dt.date(2030,1,5), dt.date(2030,1,6)]
		assert utils.group_contiguous_points(test_dates) == [
			(dt.date(2030,1,1), dt.date(2030,1,3)),
			(dt.date(2030,1,5), dt.date(2030,1,6))
		]

	def test_for_repeated_dates(self):
		test_dates = [dt.date(2030,1,1), dt.date(2030,1,1), dt.date(2030,1,2), dt.date(2030,1,5), dt.date(2030,1,6)]
		assert utils.group_contiguous_points(test_dates) == [
			(dt.date(2030,1,1), dt.date(2030,1,2)),
			(dt.date(2030,1,5), dt.date(2030,1,6))
		]

	def test_for_repeated_same_date(self):
		test_dates = [dt.date(2030,1,1), dt.date(2030,1,1), dt.date(2030,1,1), dt.date(2030,1,1), dt.date(2030,1,1)]
		assert utils.group_contiguous_points(test_dates) == [
			(dt.date(2030,1,1), dt.date(2030,1,1))
		]