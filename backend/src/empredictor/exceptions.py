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
