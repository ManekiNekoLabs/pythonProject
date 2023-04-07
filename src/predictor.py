import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Bidirectional, LSTM
from sklearn.preprocessing import MinMaxScaler

# load the dataset
df = pd.read_csv('solana.csv')

# select the columns needed for training
df = df[['close']]

# convert the dataframe to a numpy array
data = df.values

# scale the data

scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)


# create a function to create a dataset with look back
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


# create the dataset with look back of 600 days
look_back = 600
x_train, y_train = create_dataset(data, look_back)

# reshape the input data to be [samples, time steps, features]
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# create and fit the Bi-LSTM network
model = Sequential()
model.add(Bidirectional(LSTM(50, input_shape=(look_back, 1))))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=100, batch_size=1, verbose=2)

# make a prediction for the 30 days
last_600_days = data[-600:]
next_week = []
for i in range(90):
    next_day = model.predict(last_600_days.reshape(1, -1, 1))
    next_week.append(next_day[0, 0])
    last_600_days = np.append(last_600_days[1:], next_day, axis=0)

# unscale the predicted data
next_week = scaler.inverse_transform(np.array(next_week).reshape(-1, 1))

# plot the predicted data
plt.plot(next_week)
plt.title('Price Prediction for 90 days')
plt.xlabel('Day')
plt.ylabel('Price (USD)')
plt.show()

# print the predicted data
print("Price Prediction for 90 days:")
print(next_week)
