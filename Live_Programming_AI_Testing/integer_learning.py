import pandas as pd
import random

import  numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('int_function_data.csv')
X = df.drop(["plus", "times", "subtract"], axis=1).values
Y = df.apply(lambda s: s[2:], axis=1).values



X_change = X.tolist()
Y_change = Y.tolist()
X_new = []
Y_new = []
for index, elem in enumerate(X_change):
    if elem[0] != 1 and elem[0] != 20:
        Y_new.append(Y_change[index])
        elem1 = elem.copy()
        elem1.append((X[index+1][1]-X[index-1][1])/2)
        X_new.append(elem1)

Y_new = np.array(Y_new)
X_new = np.array(X_new)
print(X_new)
X_train, X_test, y_train, y_test = train_test_split(X_new, Y_new, test_size=0.4, random_state=1)



# print(X_train)
# print(type(y_train[0]))
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score

# Create KNN classifier
model = MLPClassifier()
model1 = DecisionTreeClassifier()
model2 = KNeighborsClassifier()
model3 = ExtraTreesClassifier()
# Fit the classifier to the data
#model.fit(X_train,y_train)
# model1.fit(X_train,y_train)
# model2.fit(X_train,y_train)
model3.fit(X_train,y_train)



#print(model.score(X_test, y_test))
#print(model1.score(X_test, y_test))
#print(model2.score(X_test, y_test))
print(model3.score(X_test, y_test))
#print(X_test[10], y_test[10])
print(model3.predict([[2, 10, 2]]))
print(f1_score(y_test, model3.predict(X_test), average='samples'))

# from sklearn.externals.six import StringIO
# from IPython.display import Image
# from sklearn.tree import export_graphviz
# import pydotplus
# dot_data = StringIO()
# export_graphviz(model1, out_file=dot_data,
#                 filled=True, rounded=True,
#                 special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
# Image(graph.create_png())