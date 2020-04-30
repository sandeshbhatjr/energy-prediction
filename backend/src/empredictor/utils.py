import datetime as dt
import numpy as np

def dateRange(startDate, endDate):
	currentDate = startDate
	while (endDate > currentDate):
		yield currentDate
		currentDate = currentDate + dt.timedelta(days=1)

def group_contiguous_points(datetime_list, day_intervals=1):
	if len(datetime_list) == 0:
		return []
	# convert to numpy array for convenience
	datetime_list.sort() # needs to be sorted to work
	datetime_array = np.array(datetime_list)
	reversed_datetime_array = np.flip(datetime_array)
	forward_difference = (datetime_array[1:] - datetime_array[:-1])
	backward_difference = np.flip(reversed_datetime_array[1:] - reversed_datetime_array[:-1])
	contiguous_forward_mask = np.concatenate([[True], (forward_difference > dt.timedelta(days=1))])
	contiguous_backward_mask = np.concatenate([(backward_difference < dt.timedelta(days=-1)), [True]])
	# zip the index of True
	contiguous_index = np.concatenate([np.where(contiguous_forward_mask), np.where(contiguous_backward_mask)]).T
	contiguous_datetimes = [(datetime_list[i1], datetime_list[i2]) for (i1, i2) in contiguous_index.tolist()]
	return contiguous_datetimes

# Daylight Savings Time utilities
# EU specific
def when_is_last_sunday_of_march_and_october(year):
	# get day of last date
	end_of_march = (dt.datetime(year, 4, 1) - dt.timedelta(days=1))
	end_of_october = (dt.datetime(year, 11, 1) - dt.timedelta(days=1))
	# some modular arithmetic to compute how far it is from the last Sunday
	days_after_last_sunday_of_march = (end_of_march.weekday() + 1) % 7
	days_after_last_sunday_of_october = (end_of_october.weekday() + 1) % 7
	last_sunday_of_march = end_of_march - dt.timedelta(days=days_after_last_sunday_of_march)
	last_sunday_of_october = end_of_october - dt.timedelta(days=days_after_last_sunday_of_october)
	return last_sunday_of_march.date(), last_sunday_of_october.date()