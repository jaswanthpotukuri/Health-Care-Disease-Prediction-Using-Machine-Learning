#!/usr/bin/env python
# coding: utf-8

# In[16]:



# Importing libraries

import numpy as np
import pandas as pd
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[17]:


# Reading the train.csv by removing the 
# last column since it's an empty column

DATA_PATH = "Training.csv"

data = pd.read_csv(DATA_PATH).dropna(axis = 1)
 
# Checking whether the dataset is balanced or not

disease_counts = data["prognosis"].value_counts()

temp_df = pd.DataFrame({

    "Disease": disease_counts.index,

    "Counts": disease_counts.values
})
 

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(temp_df["Disease"], temp_df["Counts"], color='skyblue')
plt.title('Counts of Each Disease')
plt.xlabel('Disease')
plt.ylabel('Counts')
plt.xticks(rotation=90)  # Rotating x-axis labels for better readability
plt.tight_layout()
plt.show()


# In[18]:


# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())


# In[19]:


# Encoding the target value into numerical
# value using LabelEncoder

encoder = LabelEncoder()

data["prognosis"] = encoder.fit_transform(data["prognosis"])


# In[20]:



X = data.iloc[:,:-1]

y = data.iloc[:, -1]

X_train, X_test, y_train, y_test =train_test_split(

  X, y, test_size = 0.2, random_state = 24)
 

print(f"Train: {X_train.shape}, {y_train.shape}")

print(f"Test: {X_test.shape}, {y_test.shape}")


# In[22]:


# Defining scoring metric for k-fold cross validation

def cv_scoring(estimator, X, y):

    return accuracy_score(y, estimator.predict(X))
 
# Initializing Models

models = {

    "SVC":SVC(),

    "Gaussian NB":GaussianNB(),

    "Random Forest":RandomForestClassifier(random_state=18)
}
 
# Producing cross validation score for the models

for model_name in models:

    model = models[model_name]

    scores = cross_val_score(model, X, y, cv = 10, 

                             n_jobs = -1, 

                             scoring = cv_scoring)

    print("=="*30)

    print(model_name)

    print(f"Scores: {scores}")

    print(f"Mean Score: {np.mean(scores)}")


# In[23]:


# Training and testing SVM Classifier
svm_model = SVC()
svm_model.fit(X_train, y_train)
preds = svm_model.predict(X_test)

print(f"Accuracy on train data by SVM Classifier: {accuracy_score(y_train, svm_model.predict(X_train))*100}")

print(f"Accuracy on test data by SVM Classifier: {accuracy_score(y_test, preds)*100}")

# Function to plot confusion matrix
def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False,
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()
    
# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, preds)

# Plot confusion matrix
plot_confusion_matrix(conf_matrix)

# Training and testing Naive Bayes Classifier
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
preds = nb_model.predict(X_test)
print(f"Accuracy on train data by Naive Bayes Classifier: {accuracy_score(y_train, nb_model.predict(X_train))*100}")

print(f"Accuracy on test data by Naive Bayes Classifier: {accuracy_score(y_test, preds)*100}")

# Function to plot confusion matrix
def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False,
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()
# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, preds)
# Plot confusion matrix
plot_confusion_matrix(conf_matrix)

# Training and testing Random Forest Classifier
rf_model = RandomForestClassifier(random_state=18)
rf_model.fit(X_train, y_train)
preds = rf_model.predict(X_test)
print(f"Accuracy on train data by Random Forest Classifier: {accuracy_score(y_train, rf_model.predict(X_train))*100}")

print(f"Accuracy on test data by Random Forest Classifier: {accuracy_score(y_test, preds)*100}")
# Function to plot confusion matrix
def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False,
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()
# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, preds)
# Plot confusion matrix
plot_confusion_matrix(conf_matrix)


# In[8]:


# Training the models on whole data
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
final_svm_model.fit(X, y)
final_nb_model.fit(X, y)
final_rf_model.fit(X, y)

# Reading the test data
test_data = pd.read_csv("Testing.csv").dropna(axis=1)

test_X = test_data.iloc[:, :-1]
test_Y = encoder.transform(test_data.iloc[:, -1])

# Making prediction by take mode of predictions 
# made by all the classifiers
svm_preds = final_svm_model.predict(test_X)
nb_preds = final_nb_model.predict(test_X)
rf_preds = final_rf_model.predict(test_X)

final_preds = [mode([i,j,k])[0][0] for i,j,
k in zip(svm_preds, nb_preds, rf_preds)]

print(f"Accuracy on Test dataset by the combined model: {accuracy_score(test_Y, final_preds)*100}")
# Function to plot confusion matrix
def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False,
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()
# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, preds)
# Plot confusion matrix
plot_confusion_matrix(conf_matrix)


# In[9]:




from statistics import mode

def predictDisease(symptoms):
   symptoms = symptoms.split(",")
   # Debugging statement: print the symptoms extracted from the input
   print("Input symptoms:", symptoms)
   
   # creating input data for the models
   input_data = [0] * len(data_dict["symptom_index"])
   for symptom in symptoms:
        # Debugging statement: print symptom before and after capitalization
        print("Symptom before capitalization:", symptom)
        symptom = " ".join([i.capitalize() for i in symptom.strip().split("_")])
        print("Symptom after capitalization:", symptom)
        
        if symptom in data_dict["symptom_index"]:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1
        else:
            print(f"Symptom '{symptom}' not found in the symptom index dictionary.")

   # reshaping the input data and converting it
   # into suitable format for model predictions
   input_data = np.array(input_data).reshape(1,-1)
   
   # generating individual outputs
   rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
   nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
   svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

   # making final prediction by taking mode of all predictions
   final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
   predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
   }
   # Displaying predictions
   print("RF Model Prediction:", rf_prediction)
   print("Naive Bayes Prediction:", nb_prediction)
   print("SVM Model Prediction:", svm_prediction)
   print("Final Prediction:", final_prediction)
   
   return predictions

# Testing the function
print(predictDisease("stomach_pain, acidity, ulcers_on_tongue, chest_pain"))


# In[ ]:




