class RequestFailure(Exception):
	def __init__(self, message, status_code=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
	def to_dict(self):
		res_dict = { 'msg' : self.message }
		return res_dict

class IncorrectAPIKey(Exception):
	pass

class DataNotRetrieved(Exception):
	pass

class InvalidTimeSlots(Exception):
	def __init__(self, message, dates_of_incorrect_entries):
		super().__init__(self, message)
		self.message = message
		self.dates_of_incorrect_entries = dates_of_incorrect_entries

class MoreThanOneContiguousDatapoint(Exception):
	def __init__(self, message, non_contiguous_time_slots):
		super().__init__(self, message)
		self.message = message
		self.non_contiguous_time_slots = non_contiguous_time_slots