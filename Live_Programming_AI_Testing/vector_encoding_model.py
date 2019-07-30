from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, Flatten
from keras.optimizers import Adam
from shutil import copyfile
import pandas as pd
import numpy as np
import os
import time
from sklearn.model_selection import train_test_split
import json


def removeFunctionsFromGrammar(functionsToKeep, path_to_file):
    with open(path_to_file) as oldfile, open('tester.sl', 'w') as newfile:
        writeAll = False
        newfile.write("(set-logic SLIA)\n\n\n(synth-fun f ((name String)) String\n((Start String (ntString))\n")
        for num, line in enumerate(oldfile):
            if num > 7:
                if writeAll:
                    newfile.write(line)
                elif "(ntBool Bool (true false" in line:
                    newfile.write(line)
                    writeAll = True
                elif any(function_ in line for function_ in functionsToKeep) or (line.count('(') != 1 and line.count(')\n') != 1):
                    newfile.write(line)
                elif line.count(')') >= 3 and line.count('(') == 1:
                    newfile.write('))')



def testModel(benchmarks_json_file, model_to_test, k):
    results = {}
    possibleFunctions = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len",
                         "str.to.int", "str.indexof"]

    with open(benchmarks_json_file) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            results[key] = model_to_test.predict_proba(np.array(value))
            voting_array = []
            for i, elem in enumerate(results[key]):
                predicted_value_2 = [1 for v in range(len(possibleFunctions))]
                idx = np.argpartition(elem, k)
                for index in idx[:k]:
                    predicted_value_2[index] = 0
                for j, element in enumerate(predicted_value_2):
                    if element == 1:
                        voting_array.append(possibleFunctions[j])
            f_count = {}
            for f in voting_array:
                if f in f_count.keys():
                    f_count[f] += 1
                else:
                    f_count[f] = 1

            functions_to_keep = sorted(f_count.items(), key=lambda kv: kv[1])[0:len(possibleFunctions)-k]
            functions_to_keep = [i[0] for i in functions_to_keep]
            removeFunctionsFromGrammar(functions_to_keep, "/Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
            times = []
            print(key)
            startTime = time.time()
            os.system("cvc4 --tlimit=10000 /Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
            times.append(time.time()-startTime)
            startTime = time.time()
            os.system("cvc4 --tlimit=10000 /Users/kairotieremorton/Documents/Code/Random\ Python\ Code/AI/Supervised\ Learning/Live\ Programming\ Yale\ Project/Live_Programming_AI_Testing/tester.sl")
            times.append(time.time() - startTime)
            print(times)
            results[key] = times
        return results







# df = pd.read_csv('string_data_full.csv')
#
# # df = pd.read_pickle("string_data_compressed.pickle")
#
# # seperate input data from labels
# X_extracted = df.drop(df.columns[[40, 41, 42, 43, 44, 45, 46, 47, 48, 49]], axis=1).values
# Y_extracted = df.apply(lambda s: s[40:], axis=1).values
#
#
#
# X_train, X_test, y_train, y_test = train_test_split(X_extracted, Y_extracted, test_size=0.2, random_state=3)
#
# print(X_test.shape)

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

# model = Sequential()
# model.add(Embedding(input_dim=59, input_length=40, output_dim=100))
# model.add(Flatten())
# model.add(Dense(256, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(256, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(256, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(10, activation='sigmoid'))
#
# adam = Adam(lr=0.001)
# model.compile(loss='binary_crossentropy',
#               optimizer=adam, metrics=['accuracy'])
#
# model.fit(X_train, y_train, epochs=20, batch_size=200, validation_data=(X_test, y_test))
#
# model.save("model_keras.h5")
# print("model saved")

model = load_model("model_keras.h5")


print(testModel("benchmarks.json", model, 2))

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
