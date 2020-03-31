from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from entsoe import EntsoePandasClient
# import workalendar # for later
import datetime as dt
import pandas as pd
import secret

days_in_week_list = [
	'Monday',
	'Tuesday',
	'Wednesday',
	'Thursday',
	'Friday',
	'Saturday',
	'Sunday'
]

# load API key
try:
	API_KEY = secret.API_KEY
except(error):
	print(error)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/daprices/<dateChosen>')
@cross_origin()
def get_daprice(dateChosen):
	da_price_dict = {}
	try:
		day = int(dateChosen[6:8])
		month = int(dateChosen[4:6])
		year = int(dateChosen[:4])
	except(ValueError):
		return jsonify({
			'err': 'Your input date is not in the right format'
		})

	dateChosen_as_date_object = dt.datetime(year,month,day)

	# check cache first
	# TO BE IMPLEMENTED!

	# else retrieve
	client = EntsoePandasClient(api_key=API_KEY)

	da_price_dict['date'] = dateChosen

	da_price_dict['weekday'] = days_in_week_list[dateChosen_as_date_object.weekday()]

	start = pd.Timestamp(dateChosen_as_date_object, tz='Europe/Brussels')
	end = pd.Timestamp(dateChosen_as_date_object + dt.timedelta(days=1), tz='Europe/Brussels')

	# choose bidding zone
	bidding_zone = 'DE-LU'
	country_code = 'DE-LU'

	da_price_dict['bidding zone'] = 'DE-LU'

	da_price_list = client.query_day_ahead_prices(country_code, start=start, end=end).to_list()
	da_price_dict['hourly data'] = dict(enumerate(da_price_list))

	return jsonify(da_price_dict)

@app.route('/predict/<model>/<dateChosen>')
def predict(model, dateChosen):
	pass

if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)