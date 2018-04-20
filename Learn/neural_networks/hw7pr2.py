

# !conda update scikit-learn

import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
from sklearn.neural_network import MLPClassifier

import numpy as np
import pandas as pd


print("+++ Start of digits problem +++\n")
# For Pandas's read_csv, use header=0 when you know row 0 is a header row
# df here is a "dataframe":
df = pd.read_csv('digits.csv', header=0)    # read the file
df.head()                                 # first few lines
df.info()                                 # column details

#no data transformation needed

print("+++ Converting to numpy arrays... +++")
# Data needs to be in numpy arrays - these next two lines convert to numpy arrays
X_data_complete = df.iloc[:,0:64].values         # iloc == "integer locations" of rows/cols
y_data_complete = df[ '64' ].values       # individually addressable columns (by name)

X_partial_complete = df.iloc[:,0:39].values #represent column that are filled for partially unfilled digits
y_partial_complete = y_data_complete #the same as y_data_complete

X_partial_unknown = X_partial_complete[:10,:] #first 10 digits are partially unfilled digits
y_partial_unknown = y_partial_complete[:10]

X_full_unknown = X_data_complete[10:22,:] #fully filled but have unknown target
y_full_unknown = y_data_complete[10:22]

X_known = X_data_complete[22:,:] #fully filled and have known target
y_known = y_data_complete[22:] 

X_partial_known = X_partial_complete[22:,:] #partially filled and have known target
y_partial_known = y_partial_complete[22:]

#
# we can scramble the remaining data if we want to (we do)
# 
KNOWN_SIZE = len(y_known)
indices = np.random.permutation(KNOWN_SIZE)  # this scrambles the data each time
X_known = X_known[indices]
y_known = y_known[indices]

#scarmble the partial data as well
X_partial_known = X_partial_known[indices]
y_partial_known = y_partial_known[indices]

#
# from the known data, create training and testing datasets
#
TRAIN_FRACTION = 0.85
TRAIN_SIZE = int(TRAIN_FRACTION*KNOWN_SIZE)
TEST_SIZE = KNOWN_SIZE - TRAIN_SIZE   # not really needed, but...
X_train = X_known[:TRAIN_SIZE]
y_train = y_known[:TRAIN_SIZE]

X_test = X_known[TRAIN_SIZE:]
y_test = y_known[TRAIN_SIZE:]

#creating training and testing for partially filled digits data
X_partial_train = X_partial_known[:TRAIN_SIZE] 
y_partial_train = y_partial_known[:TRAIN_SIZE]

X_partial_test = X_partial_known[TRAIN_SIZE:]
y_partial_test = y_partial_known[TRAIN_SIZE:]

#
# it's important to keep the input values in the 0-to-1 or -1-to-1 range
#    This is done through the "StandardScaler" in scikit-learn
# 
USE_SCALER = True
if USE_SCALER == True:
    from sklearn.preprocessing import StandardScaler
    #scale the full digits 
    scaler = StandardScaler()
    scaler.fit(X_train)   # Fit only to the training dataframe
    # now, rescale inputs -- both testing and training
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    X_full_unknown = scaler.transform(X_full_unknown)

    #scale the partial digits 
    scaler_partial = StandardScaler()
    scaler_partial.fit(X_partial_train)

    X_partial_train = scaler_partial.transform(X_partial_train)
    X_partial_test = scaler_partial.transform(X_partial_test)
    
    X_partial_unknown = scaler_partial.transform(X_partial_unknown)

# scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html 
#
# mlp = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=400, alpha=1e-4,
#                     solver='sgd', verbose=10, tol=1e-4, random_state=1)

#full observations
mlp = MLPClassifier(hidden_layer_sizes=(10,10), max_iter=200, alpha=1e-4,
                    solver='sgd', verbose=True, shuffle=True, early_stopping = False, # tol=1e-4, 
                    random_state=None, # reproduceability
                    learning_rate_init=.1, learning_rate = 'adaptive')

#partial observations
mlp_partial = MLPClassifier(hidden_layer_sizes=(10,10), max_iter=200, alpha=1e-4,
                    solver='sgd', verbose=True, shuffle=True, early_stopping = False, # tol=1e-4, 
                    random_state=None, # reproduceability
                    learning_rate_init=.1, learning_rate = 'adaptive')


print("\n\n++++++++++  TRAINING  +++++++++++++++\n\n")
mlp.fit(X_train, y_train)
mlp_partial.fit(X_partial_train, y_partial_train)


print("\n\n++++++++++++  TESTING  +++++++++++++\n\n")
print("Training set score (full_digits): %f" % mlp.score(X_train, y_train))
print("Test set score (full_digits): %f" % mlp.score(X_test, y_test))

print("Training set score (partial_digits): %f" % mlp_partial.score(X_partial_train, y_partial_train))
print("Test set score (partial_digits): %f" % mlp_partial.score(X_partial_test, y_partial_test))

# let's see the coefficients -- the nnet weights!
# CS = [coef.shape for coef in mlp.coefs_]
# print(CS)

print("\n\n++++++++++++  Predictions for fully Filled Digits Obervations  +++++++++++++\n\n")
# predictions:
predictions = mlp.predict(X_test)
from sklearn.metrics import classification_report,confusion_matrix
print("\nConfusion matrix:")
print(confusion_matrix(y_test,predictions))

print("\nClassification report")
print(classification_report(y_test,predictions))

# unknown data rows...
#
unknown_predictions = mlp.predict(X_full_unknown)
print("Unknown predictions for fully filled digits:")
print("  Correct values:   [9 9 5 5 6 5 0 9 8 9 8 4]")
print("  Our predictions: ", unknown_predictions)


print("\n\n++++++++++++  Predictions for Partially Filled Digits Obervations  +++++++++++++\n\n")
# predictions:
predictions = mlp_partial.predict(X_partial_test)
from sklearn.metrics import classification_report,confusion_matrix
print("\nConfusion matrix:")
print(confusion_matrix(y_partial_test,predictions))

print("\nClassification report")
print(classification_report(y_partial_test,predictions))

# unknown data rows...(full)
#
unknown_predictions = mlp_partial.predict(X_partial_unknown)
print("Unknown predictions for partially filled digits:")
print("  Correct values:   [0 0 0 1 7 2 3 4 0 1]")
print("  Our predictions: ", unknown_predictions)

if False:
    L = [5.2, 4.1, 1.5, 0.1]
    row = np.array(L)  # makes an array-row
    row = row.reshape(1,4)   # makes an array of array-row
    if USE_SCALER == True:
        row = scaler.transform(row)
    print("\nrow is", row)
    print("mlp.predict_proba(row) == ", mlp.predict_proba(row))

# C = R.reshape(-1,1)  # make a column!

""" Comments:
1. Compared to the other algorithms we have used (Nearest neighbors, Decision Trees 
RandomForests), NNets turn out to work out extremely well, predicting with an accuracy 
of around 95% for complete data and around 90% for incomplete data. The other algorithms 
can only achieve about 70-80% accuracy. 

2. I think Neural Networks would be the best at handling incomplete data because it 
can automatically reenginner the weights of the features, where as the other algorithms 
can't and require human manipulations. 

"""