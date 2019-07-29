from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, Flatten
from keras.optimizers import Adam
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.datasets import mnist
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
import pickle
df = pd.read_csv('string_data_subtracted.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
X_extracted = df.drop(df.columns[[40, 41, 42, 43, 44, 45, 46, 47, 48, 49]], axis=1).values
Y_extracted = df.apply(lambda s: s[40:], axis=1).values



X_train, X_test, y_train, y_test = train_test_split(X_extracted, Y_extracted, test_size=0.2, random_state=3)

# counts = [0 for i in range(10)]
# for row in y_train:
#     for index, entry in enumerate(row):
#         counts[index] += entry
#
# for count in counts:
#     print(count/len(y_train))
# print("test data")
#
#
#
# counts = [0 for i in range(10)]
# for row in y_test:
#     for index, entry in enumerate(row):
#         counts[index] += entry
#
# for count in counts:
#     print(count/len(y_test))
#
#
model = Sequential()
model.add(Embedding(input_dim=59, input_length=40, output_dim=100))
model.add(Flatten())
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(10, activation='sigmoid'))

adam = Adam(lr=0.001)
model.compile(loss='binary_crossentropy',
              optimizer=adam, metrics=['accuracy'])

model.fit(X_train, y_train, epochs=50, batch_size=500, validation_data=(X_test, y_test))

model.save("model_keras.h5")
print("model saved")

# model = load_model("model_keras.h5")
# counter = 0
# k=2
#
# predicted_value = model.predict_proba(X_test)
# #print(predicted_value[0])
#
#
#     # predicted_value_2 = [1,1,1,1]
#     #predicted_value_2 = [0,0,0,0]
#
#
#
#     #for index, num in enumerate(predicted_value[0]):
#         # if num > 0.1:
#         #     predicted_value_2[index] = 1
# for i, value in enumerate(predicted_value):
#     predicted_value_2 = [1 for v in range(10)]
#     # print(value)
#     # print(y_test[i])
#     idx = np.argpartition(value, k)
#     for index in idx[:k]:
#         #print(index)
#         predicted_value_2[index] = 0
#     one_pos_true = [j for j, elem in enumerate(y_test[i]) if elem == 1]
#     one_pos_pred = [k for k, element in enumerate(predicted_value_2) if element == 1]
#     # print(one_pos_true)
#     # print(one_pos_pred)
#     if set(one_pos_true).issubset(set(one_pos_pred)) and len(one_pos_pred) != 10:
#         counter += 1
# print(counter/len(X_test))
