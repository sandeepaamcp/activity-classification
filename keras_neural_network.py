# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 17:28:43 2022

@author: PQV
"""
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler


# load the dataset
data_train = pd.read_csv("train_file.csv", header= 0, usecols=[*range(1,26)], sep=",")
data_test = pd.read_csv("test_file.csv", header= 0, usecols=[*range(1,26)], sep=",")
data_train.dropna(axis = 0, inplace = True)
data_test.dropna(axis = 0, inplace = True)

output_train = [[0,0,0]]*data_train.shape[0]
col = data_train.iloc[:,24]
for i, num in enumerate(col):
    temp = [0,0,0]
    temp[num-1]=1
    output_train[i] = temp  


output_test = [[0,0,0]]*data_test.shape[0]
col = data_test.iloc[:,24]
for i, num in enumerate(col):
    temp = [0,0,0]
    temp[num-1]=1
    output_test[i] = temp

data_train = data_train.drop(columns=['output'])
data_test = data_test.drop(columns=['output'])

#print (data_test.head())

## Scale the data
scaler = StandardScaler()
scaler.fit(data_train)
# Apply transform to both the training set and the test set.
data_train = scaler.transform(data_train)
data_test = scaler.transform(data_test)

input_train = data_train
output_train = np.array(output_train)
input_test = data_test
output_test = np.array(output_test)

# define the keras model
model = Sequential()
model.add(Dense(12, input_shape=(24,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(3, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(input_train, output_train, epochs=150, batch_size=10)
# evaluate the keras model
_, accuracy = model.evaluate(input_train, output_train)
print('Accuracy: %.2f' % (accuracy*100))

# make class predictions with the model
predictions = (model.predict(input_test) > 0.5).astype(int)

# summarize the first 5 cases
for i in range(0,len(data_test)):
	print('%s (expected %s)' % (predictions[i].tolist(), output_test[i].tolist()))
    
print ('nb_data_test', len(data_test))
