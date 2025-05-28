import numpy as np
import pandas as pd

# Load the diabetes dataser

diabetes =  pd.read_csv('diabetes.csv')

diabetes

# Import necessary Libraries

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#Assuming the target variable is the last column in the diabetes dataset

x = diabetes.iloc[:, :-1].values

y = diabetes.iloc[:, -1].values

#Split the data into training & testing set

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

#Create a Logistic Regression classifier

classifier = LogisticRegression(max_iter=1000)

# Train the classifier on the training data

classifier.fit(x_train, y_train)

#Make predictions on the test data

y_pred = classifier.predict(x_test)

#Evaluate the classifier

accuracy = accuracy_score(y_test, y_pred)

confusion = confusion_matrix(y_test, y_pred)

classification_rep = classification_report(y_test, y_pred)

print("Accuracy: {:.2f}%".format(accuracy * 100))

print("Confusion Matrix:\n", confusion)

print("Classification Report:\n", classification_rep)