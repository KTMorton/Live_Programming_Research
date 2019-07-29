import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from tpot import TPOTClassifier

# import data from file into pandas dataFrame
#df = pd.read_csv('string_data.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
# X = df.drop(df.columns[[416, 417, 418, 419]], axis=1).values
# Y = df.apply(lambda s: s[416:], axis=1).values

df = pd.read_csv('string_data_2.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
X = df.drop(df.columns[[688, 689, 690, 691, 692, 693, 694, 695, 696, 697]], axis=1).values
Y = df.apply(lambda s: s[688:], axis=1).values


#Y.resize((df.shape[0], ))

# df.to_pickle("string_data_compressed.pickle")
# print(Y)

# split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

# Create MLP classifier and define hyperameters
model = MLPClassifier(verbose=1, learning_rate_init=0.5, hidden_layer_sizes=(344, 172, ), batch_size=500,
                       learning_rate='adaptive', activation='relu', solver='sgd', max_iter=200)
#
# model = OneVsRestClassifier(MLPClassifier(verbose=1, learning_rate_init=0.01, hidden_layer_sizes=(256, 256, 256), batch_size=200,
#                          learning_rate='adaptive', activation='sigmoid', solver='sgd', max_iter=500))
# # #model = TPOTClassifier(generations=5, population_size=50, verbosity=3)
# #
# #
# # # Fit the classifier to the data
# model.fit(X_train,y_train)

model = joblib.load('saved_model_3.pkl')
counter = 0
k=2
for i, x in enumerate(X_test):
    predicted_value = model.predict_proba([x])

    # predicted_value_2 = [1,1,1,1]
    #predicted_value_2 = [0,0,0,0]
    predicted_value_2 = [1 for v in range(10)]


    #for index, num in enumerate(predicted_value[0]):
        # if num > 0.1:
        #     predicted_value_2[index] = 1
    idx = np.argpartition(predicted_value[0], k)
    for index in idx[:k]:
        #print(index)
        predicted_value_2[index] = 0
        # predicted_value_2[predicted_value[0].tolist().index(min(predicted_value[0]))] = 0
    one_pos_true = [j for j, elem in enumerate(y_test[i]) if elem == 1]
    one_pos_pred = [k for k, element in enumerate(predicted_value_2) if element == 1]
    # print(one_pos_true)
    # print(one_pos_pred)
    if set(one_pos_true).issubset(set(one_pos_pred)) and len(one_pos_pred) != 10:
        counter += 1
print(counter/len(X_test))



# print(model.score(X_train, y_train))
# print(model.score(X_test, y_test))
#
# joblib.dump(model, 'saved_model_3.pkl')

