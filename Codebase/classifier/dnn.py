import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import os
import time
os.environ["CUDA_VISIBLE_DEVICES"]="-1"  


# columns=['date','time','username','wrist','activity','acceleration_x','acceleration_y','acceleration_z','gyro_x','gyro_y','gyro_z']
columns=['date','time','username','wrist','activity','acceleration_x','acceleration_y','acceleration_z','gyro_x','gyro_y','gyro_z','hour','minutes','seconds','microsecond', 'ordinal_time']

df = pd.read_csv('new_dataset.csv', names=columns, header=0).drop(['date','time','username','wrist'],axis=1)
labels= df.pop('activity')

X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.3,random_state=42) # 70% training and 30% test

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# Feature columns describe how to use the input.
my_feature_columns = []
for key in X_train.keys():
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))

print(my_feature_columns)

def input_fn(features, labels, training=True, batch_size=256):
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle and repeat if you are in training mode.
    if training:
        dataset = dataset.shuffle(1000).repeat()
    
    return dataset.batch(batch_size)

#Building a DNNclassifier
classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    model_dir='./model',
    # Two hidden layers of 30 and 10 nodes respectively.
    hidden_units=[30, 10],
    # The model must choose between 2 classes.
    n_classes=2)

start = time.time()
classifier.train(
    input_fn=lambda: input_fn(X_train, y_train, training=True),
    steps=10000)
stop = time.time()
print(f"Training time: {stop - start}")


eval_result = classifier.evaluate(
    input_fn=lambda: input_fn(X_test, y_test, training=False))


print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))