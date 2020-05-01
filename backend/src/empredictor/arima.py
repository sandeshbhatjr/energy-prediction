from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from .model import model

class AR_model:
	def __init__(self):
		pass
	def train(self, day_ahead_price):
		X = day_ahead_price.as_series()
		self.model = AutoReg(180, seasonal=True, trend='ct')
		self.model.select_order(180)
		self.model.fit()
		pass
	def predict(self, X):
		pass