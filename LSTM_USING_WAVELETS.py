import pandas as pd
import numpy as np
import ccxt  # Libreria que consigue los datos sobre algunas cryptomonedas en algunos exchange's
import matplotlib.pyplot as plt
import time, datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import tensorflow as tf
from keras.utils.generic_utils import get_custom_objects
from keras import backend as K
from numpy.random import seed
seed(1)
from tensorflow import keras
from keras.layers import Activation

def oscarhGaussD1(x):
    '''
    To be able to see and use the wavelet activation function consult:
                  -Dr. Herrera Oscar, Priego Belém, “deep learning, neural network, activation functions, wavelets,
                  Keras-Tensorflow”, Department of Systems, Universidad Autónoma Metropolitana Unidad
                  Azcapotzalco, 22 December 2021.
    '''
    pass

exchange = ccxt.binance()
par = 'BTC/USDT'
timeframe = '1d'  # candles time, it can be ('1m':'1minute', '1h':'1hour', '1d':'1day')
start_date = int((time.mktime(datetime.datetime(2017, 8, 17, 0,
                                                0).timetuple()) - 21600) * 1000)  # Tiempo en UNIX(ms) equivalente a la fecha de inicio == 2017-01-01-00:00:00 UTC

def get_candles(par, timeframe, start_date):
    if timeframe == '1m':
        time_increase = 60000000  # Tiempo en milisegundos equivalente a la temporalidad de velas de 1000 minutos
    elif timeframe == '1h':
        time_increase = 3600000000  # Tiempo en milisegundos equivalente a la temporalidad de velas de 1000 horas
    elif timeframe == '1d':
        time_increase = 86400000000  # Tiempo en milisegundos equivalente a la temporalidad de velas de 1000 dias

    datos = exchange.fetch_ohlcv(par, timeframe=timeframe, limit=1000, since=start_date)
    df = pd.DataFrame(datos, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    now = exchange.milliseconds()  # Fecha del ahora en tiempo unix convertir a fecha normal con pd.to_datatime(now, unit='ms')

    while start_date < now:
        datos = exchange.fetch_ohlcv(par, timeframe=timeframe, limit=1000, since=start_date + time_increase)
        fer = pd.DataFrame(datos, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        df = pd.concat([df, fer], ignore_index=True)
        start_date += time_increase  # Tiempo en milisegundos equivalente al tiempo de velas que se quiere

    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.set_index('time', drop=True)
    return df


def graphic(x_test_index, result, x_test1):
    plt.plot(x_test_index[0:len(result)], result, color='red', label='Prediction')
    plt.plot(x_test_index[0:len(result)], x_test1[time_step:len(result) + time_step], color='blue',
             label='True value')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Bitcoin data prediction using wavelet activation function called "oscarhGaussD1"')
    #plt.title('Bitcoin data prediction using ReLu activation function')
    plt.legend()
    plt.show()


df = get_candles(par, timeframe, start_date)
# print(df.head(5), df.shape)

percentage_train = 0.8

x_train = df[:int(len(df) * percentage_train)].iloc[:, 2]
x_train = np.array(x_train)
x_train = x_train[:, np.newaxis]

x_test = df[int(len(df) * percentage_train):].iloc[:, 2]
x_test_index = x_test.index
x_test = np.array(x_test)
x_test = x_test[:, np.newaxis]

x_test1 = x_test

sc = MinMaxScaler(feature_range=(0, 1))  # Normalizamos
set_train_sc = sc.fit_transform(x_train)

time_step = 50
X_train = []
Y_train = []

for i in range(0, len(set_train_sc) - time_step):  # FIRST FOR
    X_train.append(set_train_sc[i:i + time_step, 0])
    Y_train.append(set_train_sc[i + time_step, 0])

X_train, Y_train = np.array(X_train), np.array(Y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

dim_input = (X_train.shape[1], 1)
dim_output = 1
Num_a = 50

model = Sequential()
# model.add(LSTM(units=Num_a, input_shape=dim_input, activation='relu'))
model.add(LSTM(units=Num_a, input_shape=dim_input,
               activation='oscarhGaussD1'))  # units define how many outputs we want// input_shape means the dimensions of the inputs
model.add(Dense(units=dim_output))
model.compile(optimizer='rmsprop',
              loss='mse')  # "loss function" that measures how good the network's predictions are. # An "optimizer" that can tell the network how to change its weights.
model.fit(X_train, Y_train, epochs=30, batch_size=32)

x_test = sc.transform(x_test)
X_test = []

for i in range(0, len(x_test) - time_step):  # SECOND FOR
    X_test.append(x_test[i:i + time_step, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(X_test.shape)
result = model.predict(X_test)
result = sc.inverse_transform(result)

graphic(x_test_index, result, x_test1)
