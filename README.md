# energy-prediction
What is the SOTA technique for forecasting day-ahead and intraday market prices for electricity in Germany?

## Brief overview of domain knowledge

Free electricity markets are governed by a strong supply-demand dynamics. The key reason is that electricity can't be stored, so what is generated needs to be used up instantly. This makes forecasting demands essential to the business.  
From an economic standpoint, there are three key markets in which electricity is traded:

- **futures market**: the price is set (upto 6 years) in advance, though you pay a premium for this assurance,  
- **day-ahead market**: the price is set a day before,  
- **intra-day market**: the price is set upto ? minutes before?   

The project is explained in the following parts:  
1. [Data extraction and understanding](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_cleandata.ipynb)  
2. [Statistical models](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_statistical_models.ipynb)  
Additional:  
[Using facebook's forecast engine: Prophet](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_prophet.ipynb)  
3. [Deep models](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_deep.ipynb)  
Additional:  
[The Uber approach and M4 winner: ES-RNN](https://github.com/sandeshbhatjr/energy-prediction/blob/master/docs/ep_esRNN.ipynb)  
4. Analysis and discussion `WIP`  

The following techniques are attempted:  
Standard ML techniques for time-series forecasting:
1. Seasonal ARIMA model
2. ETS  and Holtz-Winter model
3. Dynamic harmonic regression
4. Prophet
  
Deep learning models:  
1. RNN, LSTM, GRU and convolutional LSTM
2. Inception Time [WIP]
3. Hybrid ES-RNN [WIP]
4. LSTM-MSNet [WIP]
