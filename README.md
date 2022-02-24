# energy-prediction
What is the SOTA technique for forecasting day-ahead and intraday market prices for electricity in Germany?  
[Live version here!](https://energy-client-dot-energy-predictor.appspot.com/)

THIS HAS BEEN STAGNANT FOR A WHILE BECAUSE I HAVE BEEN BUSY. STARTING THIS SUMMER, I PLAN TO PUT SOME EFFORT BACK INTO THIS PROJECT.

## Introduction

Free electricity markets are governed by a strong supply-demand dynamics. The key reason is that electricity can't be stored, so what is generated needs to be used up instantly. This makes forecasting demands essential to the business.  
From an economic standpoint, there are three key markets in which electricity is traded:

- **futures market**: the price is set (upto 6 years) in advance, though you pay a premium for this assurance,  
- **day-ahead market**: the price is set a day before,  
- **intra-day market**: the price is set upto 5 minutes before.   
We are interested in the prediction of day-ahead and intra-day prices; the prediction window is at minimum one day in advance, but some of the algorithms naturally extend to bigger window sizes (with increasing errors as we go farther).

The project is explained in the following parts:  
1. [Data extraction and understanding](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_cleandata.ipynb)  
2. [Statistical models](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_statistical_models.ipynb)  
Additional:  
[Using facebook's forecast engine: Prophet](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_prophet.ipynb)  
3. [Deep models](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_deep.ipynb)  

4. Analysis and discussion `WIP`  

## Getting started

The project consists of a few parts: the notebooks in `/docs`, the backend predictor in `/backend` and a frontend client for visualisation in `/energy-viz-app`. The notebooks are basically Jupyter notebooks which form the core of the explanation of the data analysis method. The backend takes care of managing the prediction task as a service, and is written in Python. The frontend client is written in React, using d3.js for visualisation.  

For running the backend, just install from requirements.txt and run the main.py script. Expect a package to be deployed into PyPi in the near future:
```
cd backend
pip install requirements.txt
python main.py
```
It is possible to look at the results directly, though the frontend client does the job of building shiny graphs using this data in a REST-like manner. The default port of the backend is assumed to be `8080`.
```
cd energy-viz-app
npm install
npm run local
```
Alternatively, you can access a live production version [online](https://energy-client-dot-energy-predictor.appspot.com/).

## License

This project is licensed under the GNU-GPL license - see the file LICENSE for more details.

## Author

- J R Sandesh Bhat - Initial work [https://github.com/sandeshbhatjr](https://github.com/sandeshbhatjr)

## Acknowledgements

Thanks to ENTSOE Transparency Platform for providing the API key for data access.
