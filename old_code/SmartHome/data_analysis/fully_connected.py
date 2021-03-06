import tensorflow as tf
import pandas as pd
import math
import random
from sklearn import preprocessing
from sklearn.utils import shuffle
import numpy as np

np.random.seed(2)
random.seed(2)

data1 = pd.read_csv("HomeA.csv", header=None, skiprows=[0], usecols=(range(1, 2)))
data2 = pd.read_csv("HomeA.csv", header=None, skiprows=[0], usecols=(range(3, 13)))
frames = [data1, data2]
data = pd.concat(frames, axis=1)
dataset = data.values

num_features = 11
num_hidden = 128
num_classes = 1
batch_size = 16
time_steps = 10

train_size = int(dataset.shape[0] * 0.80)

#  Make dataset random from everywhere
# rows = np.arange(dataset.shape[0] - time_steps)
# np.random.shuffle(rows)
# train_rows = rows[:train_size]
# te_rows = rows[train_size:]
#
# train = dataset[train_rows, :]
# scalar = preprocessing.StandardScaler().fit(train)

# sample test dataset from the end
train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
scalar = preprocessing.StandardScaler().fit(train)
trainX = scalar.transform(train)
trainY = dataset[1:len(trainX) + 1, 0]
testX = scalar.transform(test)
testY = dataset[len(trainX) + 1:, 0]

# train = np.column_stack((trainX, trainY))[:-3, :]
train = np.column_stack((trainX, trainY))[:-3, :]
train = train.reshape(-1, time_steps, 12)

testX = testX[:-1]  # make test y same dimesnsions as test
test = np.column_stack((testX, testY))[:-8, :]
test = test.reshape(-1, time_steps, 12)

# np.random.shuffle(test)
np.random.shuffle(train)

x_ph = tf.placeholder('float', [None, time_steps - 1, num_features], name='x')
y_ph = tf.placeholder('float', [None, num_classes], name='y')
dropout_ph = tf.placeholder('float', [], name='dropout')


def next_batch(i):
    x_batch = train[i:i + batch_size, :time_steps - 1, 0:num_features]
    y_batch = train[i:i + batch_size, time_steps - 1, num_features]
    return x_batch, y_batch


def te_batch():
    x_batch = test[:, :time_steps - 1, 0:num_features]
    y_batch = test[:, time_steps - 1, num_features]
    return x_batch, y_batch.reshape(-1, 1)


def fully_connected_model(x):
    x = tf.layers.flatten(x)
    layer1 = tf.layers.dense(x, num_hidden, activation='relu')
    layer2 = tf.layers.dense(layer1, num_hidden, activation='relu')
    layer3 = tf.layers.dense(layer2, num_hidden, activation='relu')



    return tf.layers.dense(layer3, 1)


def accuracy(x, y, data_size):
    acc = 0
    for i in range(0, data_size):
        if abs(x[i] - y[i]) < 0.2:
            acc += 1
    return float(acc / data_size)


prediction = fully_connected_model(x_ph)
cost = tf.losses.huber_loss(y_ph, prediction)
optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    training_steps = 1500
    acc_arr_te = []
    acc_arr_tr = []
    loss_arr_te = []
    loss_arr_tr = []
    for epoch in range(0, training_steps):
        np.random.shuffle(train)
        for i in range(int(len(train) - batch_size)):
            batch_x, batch_y = next_batch(i)
            batch_x = batch_x.reshape((batch_size, time_steps - 1, num_features))
            batch_y = batch_y.reshape(-1, 1)
            sess.run(optimizer, feed_dict={x_ph: batch_x, y_ph: batch_y})
            c, prd = sess.run([cost, prediction], feed_dict={x_ph: batch_x, y_ph: batch_y})

        te_x, te_y = te_batch()
        loss_te = cost.eval({x_ph: te_x, y_ph: te_y})
        print('===================================================')
        print('Epoch: {}'.format(epoch))
        print('Huber Loss on Train:', c)
        print('Huber Loss on Test:', loss_te)
        # print("Prediction eval:", prediction.eval({x_ph: te_x}))
        acc_te = accuracy(prediction.eval({x_ph: te_x}), te_y, len(te_y))
        acc_tr = accuracy(prd, batch_y, len(batch_y))
        acc_arr_te.append([epoch, acc_te])
        acc_arr_tr.append(([epoch, acc_tr]))
        loss_arr_tr.append([epoch, c])
        loss_arr_te.append([epoch, loss_te])
        print("Accuracy on Train:", float(acc_tr))
        print("Accuracy on Test:", float(acc_te))

acc_arr_te = np.array(acc_arr_te)
acc_arr_tr = np.array(acc_arr_tr)
loss_arr_te = np.array(loss_arr_te)
loss_arr_tr = np.array(loss_arr_tr)
np.save("./Fully_connected/Home A/threshold0-2-st10-lr0001-batch16_te_acc.npy", acc_arr_te)
np.save("./Fully_connected/Home A/threshold0-2-st10-lr0001-batch16_tr_acc.npy", acc_arr_tr)
np.save("./Fully_connected/Home A/threshold0-2-st10-lr0001-batch16_te_loss.npy", loss_arr_te)
np.save("./Fully_connected/Home A/threshold0-2-st10-lr0001-batch16_tr_loss.npy", loss_arr_tr)
