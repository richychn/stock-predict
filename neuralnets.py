import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
from sklearn.neural_network import MLPClassifier
import math

import numpy as np
import pandas as pd

def neural_network(industry, prediction_data):
    print("+++ Start of pandas' datahandling +++\n")

    path = "IndustryResults/" + industry + ".csv"
    df = pd.read_csv(path, header=0)
    df.head()
    df.info()

    def transform_target(s):
        """ from string to number
        """
        if (s < -1):
            return 0 #represent positive growth rate
        elif (s < -0.5 and s > -1):
            return 1 #represent negative growth rate
        elif (s < -0.25 and s > -0.5):
            return 2 #represent negative growth rate
        elif (s < 0 and s > -0.25):
            return 3
        elif (s < 0.25 and s > 0):
            return 4
        elif (s > 0.25 and s < 0.5):
            return 4
        elif (s < 1 and s > 0.5):
            return 5
        else:
            return 6

    def transform_simple(x):
        if (x > 0.10):
            return 1
        elif (x < 0.10 and x > -0.10):
            return 0
        else:
            return -1
    def transform(s):
        if(s<=0):
            return -1
        else:
            return 1

    #apply one of the target transformation function
    df['growth_rate'] = df['growth_rate'].map(transform_simple)

    fill = []
    for i in range(1,27):
        feature_name = "f"+str(i)
        column_sum = df[feature_name].sum(skipna=True)
        column_count = df[feature_name].count()
        column_ave = column_sum / column_count
        fill.append(column_ave)
    
    #fill predict data 
    for i in range(len(prediction_data[0])):
        if (math.isnan(prediction_data[0][i])):
            prediction_data[0][i] = fill[i]


    print("+++ Converting to numpy arrays... +++")
    X_all = df.iloc[:,2:28].values   #features are column 2-27
    y_all = df["growth_rate"].values  #target column

    #fill in 'nan' data with averages of the corresponding column
    for i in range(X_all.shape[1]):
        col = X_all[:,i]
        for n in range(len(col)):
            if (math.isnan(col[n])):
                col[n] = fill[i]
    
    #to test whether the rows are saved
    # test = pd.DataFrame(X_all)
    # df = test.dropna()
    # test.head()
    # test.info()

    split = int(len(X_all) * 0.15) #15% of the dataset are training set
    X_labeled = X_all[split:,:]  # Marking where I want to start my training data
    y_labeled = y_all[split:]

    #Scrambling training data
    indices = np.random.permutation(len(X_labeled))
    X_data_full = X_labeled[indices]
    y_data_full = y_labeled[indices]
    X_train = X_data_full
    y_train = y_data_full

    X_test = X_all[:split,:]
    y_test = y_all[:split]
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
        prediction_data = scalar.transform(prediction_data)


# scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html 
#
# mlp = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=400, alpha=1e-4,
#                     solver='sgd', verbose=10, tol=1e-4, random_state=1)

#full observations
    mlp = MLPClassifier(hidden_layer_sizes=(10,10,5), max_iter=200, alpha=1e-4,
                        solver='sgd', verbose=True, shuffle=True, early_stopping = False, # tol=1e-4, 
                        random_state=None, # reproduceability
                        learning_rate_init=.1, learning_rate = 'adaptive')



    print("\n\n++++++++++  TRAINING  +++++++++++++++\n\n")
    mlp.fit(X_train, y_train)


    print("\n\n++++++++++++  TESTING  +++++++++++++\n\n")
    print("Training set score (full_digits): %f" % mlp.score(X_train, y_train))
    accuracy = mlp.score(X_test, y_test)
    print("Test set score (full_digits): %f" % accuracy)


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

    # prediction data
    #
    unknown_predictions = mlp.predict(prediction_data)
    print("  Our Growth Rate predictions: ", unknown_predictions)

    return unknown_predictions

#neural_network("Finance")