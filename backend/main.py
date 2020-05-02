from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import datetime as dt
import pandas as pd
import tables

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

@app.route('/')
def root():
	return jsonify({
		'desc' : 'energy-predictor backend API',
		'v' : 1,
		'endpoints' : {
			'/v1/daprices/<yyyymmdd>' : 'Day Ahead Prices in Germany',
			'/v1/model/list' : 'List of all trained models',
			'/v1/model/predict/<modelName>/<yyyymmdd>' : 'Model predictions',
			'/v1/summary/<period>/<condition>': 'Background Summary', 
		}
	})

@app.route('/v1/daprices/<dateChosen>')
@cross_origin()
def get_daprice(dateChosen):
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
	da_price = da_price_germany.get(start, end)
	da_price.set_index(da_price.index.hour, inplace=True)
	if da_price is None:
		return jsonify({'err': 'No data for this date available.'})
	return jsonify(da_price.to_dict())

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
		'VAR(k=720)' : {
			'descr' : 'Mulitvariate approach with a seasonality of 14 days.',
			'acc' : '33.67%'
		},
	}
	return jsonify(models)

@app.route('/v1/model/predict/<modelName>/<dateChosen>')
def predict(modelName, dateChosen):
	pass

@app.route('/v1/summary/<period>/<condition>')
def summarise(period, condition):
	if period == 'daily':
		df = da_price_germany.ddf.dataframe
		if (condition == 'all') or (condition is None):
			grouped_df = df.groupby(df.index.hour)
		elif condition == 'weekends':
			grouped_df = df[(df.index.weekday == 0) | (df.index.weekday == 1)].groupby(df.index.hour)

		def lq(x):
			return x.mean() - x.std()

		def uq(x):
			return x.mean() + x.std()

		summary_df = grouped_df.agg({'Day Ahead Price' : ['mean', 'min', 'max', lq, uq]})

		return jsonify(summary_df['Day Ahead Price'].to_dict())
	else:
		return jsonify({'err' : 'Specify summary period.'})

if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)