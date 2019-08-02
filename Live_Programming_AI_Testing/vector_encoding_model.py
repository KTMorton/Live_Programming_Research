from keras.models import Sequential, load_model, Model
from keras.layers import Dense, Dropout, Embedding, Flatten, Average, Input
from keras.regularizers import l1, l2
from keras.optimizers import Adam
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
    with open("preTimes.json") as json_file:
        pre_times = json.load(json_file)
    results = {}
    possibleFunctions = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len",
                         "str.to.int", "str.indexof"]

    with open(benchmarks_json_file) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            #results[key] = model_to_test.predict(np.array(value).reshape((4, len(value), 40)).tolist())
            results[key] = model.predict(np.array(value))
            # print(results[key])
            voting_array = []
            dist = [0.5, 0.25, 0.15]
            indexes = [1, 3, 8]
            for i, elem in enumerate(results[key]):
                predicted_value_2 = [1 for v in range(len(possibleFunctions))]
                for c, prob_value in enumerate(elem):
                    if prob_value < dist[c]:
                        predicted_value_2[indexes[c]] = 0
                # idx = np.argpartition(elem, k)
                # for index in idx[:k]:
                #     predicted_value_2[index] = 0
                for j, element in enumerate(predicted_value_2):
                    if element == 1:
                        voting_array.append(possibleFunctions[j])

            f_count = {}
            for f in voting_array:
                if f in f_count.keys():
                    f_count[f] += 1
                else:
                    f_count[f] = 1

            functions_to_keep = sorted(f_count.items(), key=lambda kv: kv[1])
            if len(functions_to_keep) > (len(possibleFunctions)-k):
                functions_to_keep_edited = functions_to_keep[len(functions_to_keep)-(len(possibleFunctions)-k):len(possibleFunctions)]
            else:
                functions_to_keep_edited = functions_to_keep
            functions_to_keep_edited = [i[0] for i in functions_to_keep_edited]
            # if "str.indexof" not in functions_to_keep_edited:
            #     functions_to_keep_edited.append("str.indexof")
            print(functions_to_keep_edited)
            removeFunctionsFromGrammar(functions_to_keep_edited, "/Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
            times = []
            print(key)

            # startTime = time.time()
            # os.system("timeout 10s cvc4 /Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
            # times.append(time.time()-startTime)

            times.append(pre_times[key][0])
            startTime = time.time()
            os.system("timeout 10s cvc4 /Users/kairotieremorton/Documents/Code/Random\ Python\ Code/AI/Supervised\ Learning/Live\ Programming\ Yale\ Project/Live_Programming_AI_Testing/tester.sl")
            times.append(time.time() - startTime)
            print(times)
            results[key] = times
        return results










df = pd.read_csv('string_data_full.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
# X_extracted = df.drop(df.columns[[40, 41, 42, 43, 44, 45, 46, 47, 48, 49]], axis=1).values
# # Y_extracted = df.apply(lambda s: s[40:], axis=1).values
# Y_extracted = df.iloc[:, [41, 43, 48]].values
# #
# X_train, X_test, y_train, y_test = train_test_split(X_extracted, Y_extracted, test_size=0.2, random_state=3)
# X_train_formatted = X_train.reshape((4, len(X_train), 40)).tolist()
# X_test_formatted = X_test.reshape((4, len(X_test), 40)).tolist()







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
# model.add(Dense(42, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(17, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(7, activation='sigmoid'))
# model.add(Dropout(0.1))
# model.add(Dense(3, activation='sigmoid'))
# # model_inputs = []
# for x in range(4):
#     model_inputs.append(Input(shape=(40,)))
#
# embed = Embedding(input_dim=60, input_length=40, output_dim=100, name='embedding')
# l1 = Dense(55, activation='sigmoid', name='layer1')
# drop1 = Dropout(0.2)
# l2 = Dense(32, activation='sigmoid', name='layer2')
# drop2 = Dropout(0.2)
# l3 = Dense(18, activation='sigmoid', name='layer3')
#
# embed_layers = [embed(x) for x in model_inputs]
#
# flatten_list = [Flatten()(x) for x in embed_layers]
# l1_layers = [l1(x) for x in flatten_list]
# drop1_layers = [drop1(x) for x in l1_layers]
# l2_layers = [l2(x) for x in drop1_layers]
# drop2_layers = [drop2(x) for x in l2_layers]
# l3_layers = [l3(x) for x in drop2_layers]
# ave = Average()(l3_layers)
# pred = Dense(10, activation='sigmoid')(ave)
# model = Model(inputs=model_inputs, outputs=pred)


# adam = Adam(lr=0.001)
# model.compile(loss='binary_crossentropy',
#               optimizer=adam, metrics=['accuracy'])
# #
# model.fit(X_train, y_train, epochs=10, batch_size=200, validation_data=(X_test, y_test))
#
# model.save("model_keras_2.h5")
# print("model saved")

model = load_model("model_keras_2.h5")


results_final = testModel("benchmarks.json", model, 2)
print(results_final)
valid_x = []
for x in np.arange(0.01, 11, 0.05):

    t_nn_sum = 0
    t_fg_x_sum = 0
    t_fg_sum = 0
    for key, value in results_final.items():
        t_fg_sum += value[0]
        if value[1] < x:
            t_nn_sum += value[1]
        elif value[1] > x:
            t_fg_x_sum += (min(value[0], 10-x)+x)



    if (t_nn_sum+t_fg_x_sum) < t_fg_sum:
        valid_x.append(x)
        print(x)
        print(abs((t_nn_sum + t_fg_x_sum) - t_fg_sum))
        print("\n")
print(valid_x)


counts = [0,0,0]
total_time = [0, 0]
total_count = 0
timeout_ml_count = 0
both_timeout = 0
average_faster_time = 0
for key, value in results_final.items():
    if results_final[key][0] >= 10 and results_final[key][1] >= 10:
        both_timeout += 1

    if results_final[key][0] < 10 and results_final[key][1] >= 10:
        timeout_ml_count += 1
    if results_final[key][0] < 10 and results_final[key][1] < 10:
        total_count += 1
        total_time[0] += results_final[key][0]
        total_time[1] += results_final[key][1]
        if abs(results_final[key][0]-results_final[key][1]) <= 0.1:
            counts[1] += 1
        elif results_final[key][0] < results_final[key][1]:
            counts[0] += 1
        else:
            counts[2] += 1
            print(results_final[key][1])
            average_faster_time += results_final[key][1]

    results_final[key] = ((results_final[key][0]-results_final[key][1])/results_final[key][0])*100
print(results_final)
# print(len(results_final)-total_count)
print(both_timeout)
print(timeout_ml_count)
for i, c in enumerate(counts):
    counts[i] = c/total_count
print(counts)
print(total_time)




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
