class model:
	def __init__(self, da_price):
		self.train_df, self.test_df = self.train_test_timesplit(da_price.dataframe)
	@staticmethod
	def train_test_timesplit(df, train_size=0.9, test_size=0.1):
		"""
			Returns test-train split data based on date with test chronologically later than train data.
		"""
		min_date = df.index.min()
		max_date = df.index.max()
		train_split_date = min_date + (train_size * (max_date - min_date))
		test_split_date = train_split_date + (test_size * (max_date - min_date))
		train_df = df[df.index < train_split_date]
		test_df = df[(df.index > train_split_date) & (df.index < test_split_date)]
		return train_df, test_df
	def day_forward_chaining(df, k=10):
		for i in range(1,k):
			yield self.train_test_timesplit(df, train_size=(i/k), test_size=(1/k))

# this is a simple example model
class naive_model(model):
	"""
		This is baseline model that is just meant to serve as benchmark upper-bound for the error.
	"""
	def __init__(self, da_price):
		super().init(da_price)
	def predict(self, start, end):
		return daily_dataframe.from_ml_ready_df(super().train_df)

