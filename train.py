# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1heh5QmGOjsQmG2-u-9BQhYdpO5WZGKjY
"""

!pip install --upgrade tensorflow

from platform import python_version
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout,Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D,BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback,EarlyStopping
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import random
print("Python Version :"+python_version())
print("Tensorflow Version :"+tf.version.VERSION)

N_class=10;
((Xtrain, Ytrain), (Xtest, Ytest)) = fashion_mnist.load_data()
col=Xtrain.shape[2]
row=Xtrain.shape[1]
Xtrain_d = Xtrain.reshape(Xtrain.shape[0], row*col)
Xtest_d = Xtest.reshape(Xtest.shape[0], row*col)

Xtrain_c=Xtrain.reshape(Xtrain.shape[0], row,col,1)
Xtest_c=Xtest.reshape(Xtest.shape[0], row,col,1)

Xtrain_d=Xtrain_d.astype('float32')/255
Xtest_d=Xtest_d.astype('float32')/255
Xtrain_c=Xtrain_c.astype('float32')/255
Xtest_c=Xtest_c.astype('float32')/255


print(Xtrain_d.shape)
print(Xtest_d.shape)

Ytrain = keras.utils.to_categorical(Ytrain, N_class)
Ytest = keras.utils.to_categorical(Ytest, N_class)


class EarlyStopping(Callback):
    def __init__(self, monitor='accuracy', value=1.0, verbose=0):
        super(Callback, self).__init__()
        self.monitor = monitor
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs={}):
        current = logs.get(self.monitor)
        if current is None:
            print ("Early stopping requires %s available!" % self.monitor, RuntimeWarning)

        if current < self.value:
            if self.verbose > 0:
                print("Epoch %05d: early stopping THR" % epoch)
            self.model.stop_training = True



batch_size=1000;
#DNN Model
tf.keras.backend.clear_session() 
model = Sequential()
model.add(Dense(1024, input_shape=(row*col,)))
model.add(Activation('relu'))
# model.add(Dropout(0.5))

model.add(Dense(N_class))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',optimizer=Adam(),metrics=['accuracy'])

callbacks = [EarlyStopping(monitor='accuracy',verbose=1)]

history = model.fit(Xtrain_d,Ytrain,epochs=100,batch_size=batch_size,validation_data=(Xtest_d,Ytest))
model.save('my_model.h5')

labelNames = ["top", "trouser", "pullover", "dress", "coat",
	"sandal", "shirt", "sneaker", "bag", "ankle boot"]
preds = model.predict(Xtest_d)
print("[INFO] evaluating network...")
print(classification_report(Ytest.argmax(axis=1), preds.argmax(axis=1),
	target_names=labelNames))

history.history
# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# # Plot training & validation loss values
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('Model loss')
# plt.ylabel('Loss')
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Test'], loc='upper left')
# plt.show()
model.eval





#CNN Model

model = Sequential()

model.add(Conv2D(128, (3, 3), input_shape=(row,col , 1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.5))
model.add(BatchNormalization(axis=1))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(128))
model.add(Activation('relu'))


model.add(Dense(N_class))
model.add(Activation('softmax'))

# model = tf.keras.models.load_model('my_model3.h5')

model.compile(loss='categorical_crossentropy',optimizer=Adam(),metrics=['accuracy'])

callbacks = [EarlyStopping(monitor='accuracy',verbose=1)]

history= model.fit(Xtrain_c,Ytrain,epochs=30,batch_size=batch_size,validation_data=(Xtest_c,Ytest))
model.save('my_model3.h5')

from sklearn.metrics import classification_report

labelNames = ["top", "trouser", "pullover", "dress", "coat",
	"sandal", "shirt", "sneaker", "bag", "ankle boot"]
preds = model.predict(Xtest_c)
print("[INFO] evaluating network...")
print(classification_report(Ytest.argmax(axis=1), preds.argmax(axis=1),
	target_names=labelNames))

from google.colab import files
files.download("my_model3.h5")

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()