# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 18:25:36 2022

@author: PQV
"""

from __future__ import print_function 
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

from sklearn.cluster import KMeans

#Open neccessary files
data_train = pd.read_csv("train_file.csv", header= 0, usecols=[*range(1,26)], sep=",")
data_test = pd.read_csv("test_file.csv", header= 0, usecols=[*range(1,26)], sep=",")

data = pd.concat([data_train,data_test])
data_train.dropna(axis = 0, inplace = True)
data_test.dropna(axis = 0, inplace = True)

output_test = [[0,0,0]]*data_test.shape[0]
col = data_test.iloc[:,24]

for i, num in enumerate(col):
    temp = [0,0,0]
    temp[num-1]=1
    output_test[i] = temp
output_test = np.array(output_test)

data = data.drop(columns=['avg_handshake_time', 'avg_app_response_time', 'avg_data_transfer_time','output'])

scaler = StandardScaler()

scaler.fit(data_train)
# Apply transform to both the training set and the test set.
data_train = scaler.transform(data_train)
data_test = scaler.transform(data_test)



pca = PCA(n_components = 2)
pca.fit(data_train)
data_train = pca.transform(data_train)
data_test = pca.transform(data_test)

print(data_train.shape)


#Finding the appropriate number of clusters using "elbow" method 
K = 3
kmeans_kwargs = {
   "init": "random",
   "n_init": 10,
   "max_iter": 300,
   "random_state": 42,
}

# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(data_train)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()



def kmeans_display(X, label):
    K = np.amax(label) + 1
    X0 = X[label == 0, :]
    X1 = X[label == 1, :]
    X2 = X[label == 2, :]
    
    plt.plot(X0[:, 0], X0[:, 1], 'b^', markersize = 4, alpha = .8)
    plt.plot(X1[:, 0], X1[:, 1], 'go', markersize = 4, alpha = .8)
    plt.plot(X2[:, 0], X2[:, 1], 'rs', markersize = 4, alpha = .8)

    plt.axis('equal')
    plt.plot()
    plt.show()
    
#kmeans_display(X, original_label)


kmeans = KMeans(n_clusters=3, random_state=0).fit(data_train)
print('Centers found by scikit-learn:')
print(kmeans.cluster_centers_)
pred_label = kmeans.predict(data_train)
kmeans_display(data_train, pred_label)

#print(pred_label)

centers = kmeans.cluster_centers_
label = []
nb_row =0

#Test
print('\nBegin testing:')

for row in data_test:
    a = [(row[0],row[1])]
    min_dist = cdist(a,[(centers[0][0], centers[0][1])], 'euclidean')
    min_index = 0
    for i in range(1,len(centers)):
        b = [(centers[i][0], centers[i][1])]
        if cdist(a,b,'euclidean') < min_dist:
            min_dist = cdist(a,b,'euclidean')
            min_index = i

    print('%s (expected %s)' % (min_index, output_test[nb_row].tolist()))
    nb_row+=1