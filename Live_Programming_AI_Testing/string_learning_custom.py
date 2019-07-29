
import numpy as np
import tensorflow as tf
import random
import pandas as pd
from sklearn.model_selection import train_test_split


def get_batches(size, list_of_input, list_of_labels):
    batch_x = []
    batch_y = []
    inputs = list_of_input.tolist()
    for i in range(size):
        x = random.choice(inputs)
        batch_x.append(x)
        batch_y.append(list_of_labels[inputs.index(x)])
    return (batch_x, batch_y)

# Hyper-parameters

learning_rate = 0.001
epochs = 300
batch_size = 350
display_step = 1
n_hidden_1 = 100
n_hidden_2 = 100
n_hidden_3 = 100
input_size = 16
num_classes = 10
# keep_prob = 1  #0.85 during training

# tf Graph input

X = tf.placeholder("float", [None, input_size])
Y = tf.placeholder("float", [None, num_classes])
keep_prob = tf.placeholder(tf.float32)

# init weights and biases

weights = {
    'w1': tf.Variable(tf.random_normal([input_size, n_hidden_1])),
    'w2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'w3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
    'out': tf.Variable(tf.random_normal([n_hidden_3, num_classes]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'b3': tf.Variable(tf.random_normal([n_hidden_3])),
    'out': tf.Variable(tf.random_normal([num_classes]))
}

# create model

def neural_net(x):
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['w1']), biases['b1']))
    drop_out1 = tf.nn.dropout(layer_1, keep_prob)
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(drop_out1, weights['w2']), biases['b2']))
    layer_3 = tf.nn.sigmoid(tf.add(tf.matmul(layer_2, weights['w3']), biases['b3']))
    out_layer = tf.nn.sigmoid(tf.matmul(layer_3, weights['out']) + biases['out'])
    return out_layer


logits = neural_net(X)

# Define error func and optimizer

loss_op = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=Y))
#loss_op = tf.reduce_mean(tf.metrics.hamming_loss)
regularizers = tf.nn.l2_loss(weights['w2']) + tf.nn.l2_loss(weights['w3'])

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# evaluate model
correct_pred = tf.equal(tf.round(logits), Y)

accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


init = tf.global_variables_initializer()

saver = tf.train.Saver()

#import dataset

# import data from file into pandas dataFrame
df = pd.read_csv('string_data_2.csv')

# df = pd.read_pickle("string_data_compressed.pickle")

# seperate input data from labels
X_extracted = df.drop(df.columns[[688, 689, 690, 691, 692, 693, 694, 695, 696, 697]], axis=1).values
Y_extracted = df.apply(lambda s: s[688:], axis=1).values

# X_extracted = df.drop(df.columns[[16, 17, 18, 19, 20, 21, 22, 23, 24, 25]], axis=1).values
# Y_extracted = df.apply(lambda s: s[16:], axis=1).values

# X = df.drop(df.columns[[624, 625, 626, 627]], axis=1).values
# Y = df.apply(lambda s: s[624:], axis=1).values
print(df.shape[1])


#Y.resize((df.shape[0], ))

# df.to_pickle("string_data_compressed.pickle")
# print(Y)

# split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X_extracted, Y_extracted, test_size=0.2, random_state=3)
print("about to start training")
#
with tf.Session() as sess:

    sess.run(init)

    for step in range(1, epochs+1):

        batch_x, batch_y = get_batches(batch_size, X_train, y_train)

        # print(batch_x[0], batch_y[0])

        sess.run(train_op, feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.7})
        if step % display_step == 0 or step == 1:

            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x, Y: batch_y, keep_prob: 1.0})
            print("Step " + str(step) + ", Minibatch Loss= " +
                  "{:.4f}".format(loss) + ", Training Accuracy= " +
                  "{:.3f}".format(acc*100) + "%")
            print("Testing Accuracy: " + str(sess.run(accuracy, feed_dict={X: X_test,
                                                                      Y: y_test, keep_prob: 1.0})*100) + "%")
    save_path = saver.save(sess, "custom_model.ckpt")

    print("Optimization Finished!")
# counter1 = 0
# k=2
# with tf.Session() as sess1:
#   # Restore variables from disk.
#     saver.restore(sess1, "custom_model.ckpt")
#     print("Model restored.")
#     #for i, input_to_network in enumerate(X_test):
#     #print(i)
#     reshaped = np.reshape(X_test, (len(X_test), 688))
#     predicted_value = sess1.run(tf.abs(neural_net(np.array(reshaped).astype('float32'))), feed_dict={keep_prob: 1.0})
#     print(predicted_value)
#     for i, value in enumerate(predicted_value):
#         predicted_value_2 = [1 for v in range(10)]
#         #print(predicted_value_2)
#         #for index, num in enumerate(value):
#             # if num > 0.1:
#             #     predicted_value_2[index] = 1
#         #predicted_value_2[value.tolist().index(min(value))] = 0
#         idx = np.argpartition(value, k)
#         for index in idx[:k]:
#             predicted_value_2[index] = 0
#         one_pos_true = [j for j, elem in enumerate(y_test[i]) if elem == 1]
#         one_pos_pred = [k for k, element in enumerate(predicted_value_2) if element == 1]
#
#         if set(one_pos_true).issubset(set(one_pos_pred)) and len(one_pos_pred) != 10:
#             counter1 += 1
#     print(counter1 / len(X_test))
#
