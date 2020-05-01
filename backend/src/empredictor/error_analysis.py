class error_analysis:
  def __init__(self, original_df, prediction_df):
    # prediction_df needs to be a dataframe of predictions in column yhat with a datetime index
    # original_df needs to be a dataframe of actual values in column y with a datetime index
    self.original_df = original_df
    self.prediction_df = prediction_df
    self.start_date = prediction_df.index.min()
    self.end_date = prediction_df.index.max()
  def residuals(self):
    yhat = prediction_df['yhat'].to_numpy()
    y = original_df['Day Ahead Price'].to_numpy()
    residual_df = np.absolute(yhat - y)
    smape_df = (2*residual_df)/(np.absolute(yhat) + np.absolute(y))
    return residual_df, smape_df
  def smape_by_hour(self):
    _, smape_df = self.residuals()
    smape_df.replace(np.inf, 0) # remove infinite values
    return smape_df.mean(axis=0, skipna=True)*100
  def total_smape(self):
    smape_by_hour = self.smape_by_hour()
    return smape_by_hour.mean(axis=1, skipna=True)