from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import datetime as dt
import pandas as pd

from empredictor.data_cleanup import daily_dataframe, da_price
from empredictor.exceptions import IncorrectAPIKey
from empredictor.bidding_zone_info import Germany
from empredictor.exceptions import RequestFailure, IncorrectAPIKey

import secret

# load the information, from cache or entsoe
API_KEY = secret.API_KEY
da_price_germany = da_price(API_KEY, Germany)

# start the flask server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'	

@app.errorhandler(RequestFailure)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/v1/daprices/<dateChosen>')
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

	start = pd.Timestamp(dt.datetime(year, month, day, 0, 0), tz='Europe/Berlin')
	end = pd.Timestamp(dt.datetime(year, month, day, 23, 0), tz='Europe/Berlin')
	da_price_index = da_price_germany.get(start, end)
	if da_price_index is None:
		return jsonify({'err': 'No data for this date available.'})
	da_price_list = da_price_index.to_list()
	da_price_dict['Day Ahead Price'] = dict(enumerate(da_price_list))

	return jsonify(da_price_dict)

@app.route('/v1/model/list')
def list_models():
	models = {
		'Naive' : {
			'descr' : 'This is used to setup a baseline performance; it is not for actual modelling.',
			'acc' : '33.67%'
		},
		'AR(k=720)' : {
			'descr' : 'Univariate approach 1 with a seasonality of 720 hours.',
			'acc' : '33.67%'
		},
	}
	return jsonify(models)

@app.route('/v1/model/predict/<modelName>/<dateChosen>')
def predict(modelName, dateChosen):
	pass

@app.route('/v1/summary/<period>')
def summarise(period):
	if period == 'daily':
		df = da_price_germany.current_ddf.dataframe
		summary_df = df.groupby(df.index.hour).mean()
		return jsonify(summary_df[['Day Ahead Price']].to_dict())
	else:
		return jsonify({'err' : 'Specify summary period.'})

if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)