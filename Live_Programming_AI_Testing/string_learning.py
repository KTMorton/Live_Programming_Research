import pandas as pd
import random

import  numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('string_data.csv')
#df = pd.read_pickle("string_data_compressed.pickle")
X = df.drop(df.columns[[627, 626, 625, 624]], axis=1).values
Y = df.apply(lambda s: s[624:], axis=1).values
print(df.shape[1])
#df.to_pickle("string_data_compressed.pickle")
# print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)



# print(X_train)
# print(type(y_train[0]))
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score

# Create MLP classifier
#model = MLPClassifier(verbose=1, learning_rate_init=0.1, hidden_layer_sizes=(300, ), batch_size=200, alpha=0.1,
#                      learning_rate='adaptive', activation='relu', solver='sgd')
model = MLPClassifier(verbose=1)

#model1 = DecisionTreeClassifier()
# model2 = KNeighborsClassifier()
# model3 = ExtraTreesClassifier()
# Fit the classifier to the data
model.fit(X_train,y_train)
# model1.fit(X_train,y_train)
# model2.fit(X_train,y_train)
# model3.fit(X_train,y_train)



print(model.score(X_test, y_test))
# print(model1.score(X_test, y_test))
# print(model2.score(X_test, y_test))
# print(model3.score(X_test, y_test))
# print(model.predict([[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]]))
#print(X_test[10], y_test[10])
#print(f1_score(y_test, model3.predict(X_test), average='samples'))