import pandas as pd
import random

import  numpy as np
from sklearn.model_selection import train_test_split

# import data from file into pandas dataFrame
df = pd.read_csv('string_data.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
X = df.drop(df.columns[[627, 626, 625, 624]], axis=1).values
Y = df.apply(lambda s: s[624:], axis=1).values
print(df.shape[1])

# df.to_pickle("string_data_compressed.pickle")
# print(Y)

# split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1)

from sklearn.neural_network import MLPClassifier


# Create MLP classifier and define hyperameters
model = MLPClassifier(verbose=1, learning_rate_init=0.1, hidden_layer_sizes=(300, ), batch_size=200, alpha=0.1,
                       learning_rate='adaptive', activation='relu', solver='sgd')


# Fit the classifier to the data
model.fit(X_train,y_train)
print(model.score(X_test, y_test))
