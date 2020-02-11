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



def testModel(benchmarks_json_file, model_to_test, k, thresholds, time_out):
    with open("preTimes.json") as json_file:
        pre_times = json.load(json_file)
    results = {}
    possibleFunctions = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len",
                         "str.to.int", "str.indexof"]

    # indexes = [1, 3, 8]
    indexes = [i for i in range(0, len(possibleFunctions))]
    with open(benchmarks_json_file) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if key != "phone-9-long.sl" and key != "initials-long.sl":
                #results[key] = model_to_test.predict(np.array(value).reshape((4, len(value), 40)).tolist())
                # startTime = time.time()
                results[key] = model_to_test.predict(np.array(value))

                thresh = thresholds
                # thresh = []
                voting_array = []
                for i, elem in enumerate(results[key]):
                    predicted_value_2 = [1 for v in range(len(possibleFunctions))]
                    for c, prob_value in enumerate(elem):
                        if prob_value < thresh[c]:
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
                # print(functions_to_keep)
                if len(functions_to_keep) > (len(possibleFunctions)-k):
                    functions_to_keep_edited = functions_to_keep[len(functions_to_keep)-(len(possibleFunctions)-k):len(possibleFunctions)]
                else:
                    functions_to_keep_edited = functions_to_keep
                functions_to_keep_edited = [i[0] for i in functions_to_keep_edited]
                # if "str.indexof" not in functions_to_keep_edited:
                #     functions_to_keep_edited.append("str.indexof")
                # print(functions_to_keep_edited)
                removeFunctionsFromGrammar(functions_to_keep_edited, "/Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
                times = []
                print(key)

                # print("\nFull Grammar")
                # startTime = time.time()
                # os.system("timeout "+str(time_out)+"s cvc4 /Users/kairotieremorton/Downloads/PBE_Strings_Track/"+key)
                # times.append(time.time()-startTime)

                print("\nReduced Grammar")
                times.append(pre_times[key][0])
                startTime = time.time()
                print(round(pre_times[key][0]+0.5))
                os.system("timeout "+str(round(pre_times[key][0]+0.5))+"s cvc4 /Users/kairotieremorton/Documents/Code/Random\ Python\ Code/AI/Supervised\ Learning/Live\ Programming\ Yale\ Project/Live_Programming_AI_Testing/tester.sl")
                times.append(time.time() - startTime)
                # print(times)
                results[key] = times

                print("\n\n")

        return results










# df = pd.read_csv('string_data_full.csv')
#
# # df = pd.read_pickle("string_data_compressed.pickle")
#
# # seperate input data from labels
# X_extracted = df.drop(df.columns[[40, 41, 42, 43, 44, 45, 46, 47, 48, 49]], axis=1).values
# Y_extracted = df.apply(lambda s: s[40:], axis=1).values
# # Y_extracted = df.iloc[:, [41, 43, 48]].values
# # #
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

model = Sequential()
model.add(Embedding(input_dim=59, input_length=40, output_dim=100))
model.add(Flatten())
model.add(Dense(56, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(31, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(18, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(10, activation='sigmoid'))

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
# # #
# model.fit(X_train, y_train, epochs=10, batch_size=200, validation_data=(X_test, y_test))
# #
# model.save("model_test_keras_2.h5")
# print("model saved")

model = load_model("model_test_keras_2.h5")
#
#
# timeout = 5000
results_final = testModel("benchmarks.json", model, 2, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 10)

# results_final = {'bikes-long-repeat.sl': [2.0767600536346436, 1.7063140869140625], 'bikes-long.sl': [1.968538761138916, 1.7608299255371094], 'bikes.sl': [1.465296983718872, 1.268219232559204], 'bikes_small.sl': [1.226557970046997, 1.2405509948730469], 'dr-name-long-repeat.sl': [0.8039507865905762, 0.7242052555084229], 'dr-name-long.sl': [0.8159759044647217, 0.726696252822876], 'dr-name.sl': [0.07066702842712402, 0.06730318069458008], 'dr-name_small.sl': [0.07819485664367676, 0.07178997993469238], 'firstname-long-repeat.sl': [0.22238802909851074, 0.16143417358398438], 'firstname-long.sl': [0.22053194046020508, 0.1457231044769287], 'firstname.sl': [0.056738853454589844, 0.057991981506347656], 'firstname_small.sl': [0.05312204360961914, 0.04663419723510742], 'initials-long-repeat.sl': [3.327038049697876, 2.5393118858337402], 'initials-long.sl': [3600.057704925537, 3600.062481880188], 'initials.sl': [0.4003620147705078, 0.24594521522521973], 'initials_small.sl': [0.2506840229034424, 0.2475428581237793], 'lastname-long-repeat.sl': [32.48848485946655, 24.91945791244507], 'lastname-long.sl': [32.39816236495972, 25.486252069473267], 'lastname.sl': [2.3084068298339844, 1.828467845916748], 'lastname_small.sl': [1.8030593395233154, 1.840238094329834], 'phone-1-long-repeat.sl': [0.5111691951751709, 0.4943830966949463], 'phone-1-long.sl': [0.4956979751586914, 0.4861459732055664], 'phone-1.sl': [0.054620981216430664, 0.049793243408203125], 'phone-10-long-repeat.sl': [149.53289103507996, 129.42587900161743], 'phone-10-long.sl': [153.32084894180298, 133.22297716140747], 'phone-10.sl': [31.229099988937378, 8.491020917892456], 'phone-10_short.sl': [8.808948040008545, 8.279015064239502], 'phone-1_short.sl': [0.050466060638427734, 0.050173044204711914], 'phone-2-long-repeat.sl': [0.7977790832519531, 0.7832341194152832], 'phone-2-long.sl': [0.7700879573822021, 0.7573130130767822], 'phone-2.sl': [0.06857109069824219, 0.06166410446166992], 'phone-2_short.sl': [0.07363605499267578, 0.07348799705505371], 'phone-3-long-repeat.sl': [1.0170114040374756, 1.0014841556549072], 'phone-3-long.sl': [1.0341861248016357, 0.9533119201660156], 'phone-3.sl': [0.15272283554077148, 0.12392902374267578], 'phone-3_short.sl': [0.11382508277893066, 0.1139059066772461], 'phone-4-long-repeat.sl': [0.933290958404541, 0.8899199962615967], 'phone-4-long.sl': [0.9447300434112549, 0.8727641105651855], 'phone-4.sl': [0.11425471305847168, 0.10125899314880371], 'phone-4_short.sl': [0.0933380126953125, 0.08550119400024414], 'phone-5-long-repeat.sl': [84.76578879356384, 33.68135404586792], 'phone-5-long.sl': [90.80672788619995, 30.00700616836548], 'phone-5.sl': [4.875214099884033, 2.2021470069885254], 'phone-5_short.sl': [3.722166061401367, 1.5060229301452637], 'phone-6-long-repeat.sl': [83.5945131778717, 25.305983066558838], 'phone-6-long.sl': [98.14970111846924, 24.754117965698242], 'phone-6.sl': [4.851982831954956, 1.9679780006408691], 'phone-6_short.sl': [3.2272109985351562, 1.224687099456787], 'phone-7-long-repeat.sl': [89.1325170993805, 26.2275230884552], 'phone-7-long.sl': [87.8300552368164, 26.154870986938477], 'phone-7.sl': [4.566045045852661, 2.034691095352173], 'phone-7_short.sl': [3.2617759704589844, 1.256845235824585], 'phone-8-long-repeat.sl': [91.03858423233032, 35.64468002319336], 'phone-8-long.sl': [108.06427597999573, 29.94093894958496], 'phone-8.sl': [4.720944166183472, 2.165008783340454], 'phone-8_short.sl': [1.611354112625122, 0.6498479843139648], 'phone-9-long-repeat.sl': [91.18507075309753, 77.01791882514954], 'phone-9-long.sl': [3600.064687013626, 3516.2091147899628], 'phone-9.sl': [12.081001996994019, 4.862329006195068], 'phone-9_short.sl': [4.882001161575317, 4.725084066390991], 'phone-long-repeat.sl': [0.1515200138092041, 0.15489482879638672], 'phone-long.sl': [0.13927984237670898, 0.14071106910705566], 'phone.sl': [0.032032012939453125, 0.03387904167175293], 'phone_short.sl': [0.029867172241210938, 0.028970003128051758]}
print(results_final)

# for key, value in results_final.items():
#     print(key + "," + str(value[0]) + "," + str(value[1]))
#
# valid_x = []
# speed_up_from_x = []
#
# for x in np.arange(0.01, timeout, 0.1):
#
#     t_nn_sum = 0
#     t_fg_x_sum = 0
#     t_fg_sum = 0
#     for key, value in results_final.items():
#         if value[1] < timeout:
#             t_fg_sum += value[0]
#             if value[1] < x:
#                 t_nn_sum += value[1]
#             elif value[1] > x:
#                 t_fg_x_sum += (min(value[0], timeout-x)+x)
#
#
#
#     if (t_nn_sum+t_fg_x_sum) < t_fg_sum:
#         valid_x.append(x)
#         speed_up_from_x.append((x, abs((t_nn_sum + t_fg_x_sum) - t_fg_sum)))
# print(sorted(speed_up_from_x, key=lambda tup: tup[1])[-1])
# print(valid_x)
#
# counts = [0,0,0]
# total_time = [0, 0]
# total_count = 0
# timeout_ml_count = 0
# both_timeout = 0
# average_time_diff = 0
#
# for key, value in results_final.items():
#     total_time[0] += results_final[key][0]
#     total_time[1] += results_final[key][1]
#     if results_final[key][0] >= timeout and results_final[key][1] >= timeout:
#         both_timeout += 1
#     elif results_final[key][1] < results_final[key][0]:
#         # average_time_diff += ((results_final[key][0]-results_final[key][1])/results_final[key][0])
#         average_time_diff += (value[0] - value[1])
#
#     if results_final[key][0] < timeout and results_final[key][1] >= timeout:
#         timeout_ml_count += 1
#     if results_final[key][0] < timeout and results_final[key][1] < timeout:
#         total_count += 1
#         # total_time[0] += results_final[key][0]
#         # total_time[1] += results_final[key][1]
#         if abs(results_final[key][0]-results_final[key][1]) <= 0.1:
#             counts[1] += 1
#         elif results_final[key][0] < results_final[key][1]:
#             counts[0] += 1
#         else:
#             counts[2] += 1
#
#
#     results_final[key] = ((results_final[key][0]-results_final[key][1])/results_final[key][0])*100
# print(results_final)
# # print(len(results_final)-total_count)
# print(both_timeout)
# print(timeout_ml_count)
# print(total_time[0]-(timeout*both_timeout), total_time[1]-(timeout*both_timeout))
# print(counts)
# for i, c in enumerate(counts):
#     counts[i] = c/total_count
# print(counts)
# print(average_time_diff/(len(results_final)-both_timeout))


# print(str(t2) + "," + str(t3) + "," + str(total_time[1]) + "," + str(timeout_ml_count))




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
