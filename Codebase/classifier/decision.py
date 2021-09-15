import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
import time

#columns=['date','time','username','wrist','activity','acceleration_x','acceleration_y','acceleration_z','gyro_x','gyro_y','gyro_z']
columns=['date','time','username','wrist','activity','acceleration_x','acceleration_y','acceleration_z','gyro_x','gyro_y','gyro_z','hour','minutes','seconds','microsecond', 'ordinal_time']

df = pd.read_csv('new_dataset.csv', names=columns, header=0).drop(['date','time','username','wrist','hour','minutes','seconds','microsecond', 'ordinal_time'],axis=1)
labels= df.pop('activity')

X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.3, random_state=42) # 70% training and 30% test

clf = DecisionTreeClassifier()

start = time.time()
clf.fit(X_train, y_train)
stop = time.time()

joblib.dump(clf,"model.pkl")

print(f"Training time: {stop - start}")

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))