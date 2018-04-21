import numpy as np
import pandas as pd
import math

from sklearn import tree
from sklearn import ensemble

def randomforest(industry, prediction_data):
    try: # different imports for different versions of scikit-learn
        from sklearn.model_selection import cross_val_score
    except ImportError:
        try:
            from sklearn.cross_validation import cross_val_score
        except:
            print("No cross_val_score!")


    print("+++ Start of pandas' datahandling +++\n")

    path = "IndustryResults/" + industry + ".csv"
    df = pd.read_csv(path, header=0)
    df.head()
    df.info()

    #feeature engineering would occur here (in the future):
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

    #creating a list of feature average
    fill = []
    for i in range(1,27):
        feature_name = "f"+str(i)
        column_sum = df[feature_name].sum(skipna=True)
        column_count = df[feature_name].count()
        column_ave = column_sum / column_count
        fill.append(column_ave)
    #print(fill)

    print("\n+++ End of pandas +++\n")

    print("+++ Start of numpy/scikit-learn +++\n")

    print("+++++ Decision Trees +++++\n\n")

    #Data needs to be in numpy arrays, converts dataframe to numpy array
    X_all = df.iloc[:,2:29].values   #features are column 2-27
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

    #
    # some labels to make the graphical trees more readable...
    #
    print("Some labels for the graphical tree:")
    feature_names = []
    for i in range(1,28):
        feature_names.append("f"+str(i))
    target_names = ['growth_rate']

    #initializing testing sets
    X_test = X_all[:split,:]
    y_test = y_all[:split]
    #
    # cross-validation and scoring to determine parameter: max_depth
    #
    max_depth_DT = 1
    max_CV_DT = 0
    for max_depth in range(1,20): #looping through max_depth to find the optimal
        # create classifier
        dtree = tree.DecisionTreeClassifier(max_depth=max_depth)
        #dtree = dtree.fit(X_train, y_train)
        scores = cross_val_score(dtree, X_train, y_train, cv=5) #5 folds
        average_cv_score_DT = scores.mean() #average the cv scores
        print("For depth=", max_depth, "average CV score = ", average_cv_score_DT)
        #determining the best depth to use
        if (max_CV_DT < average_cv_score_DT):
            max_CV_DT = average_cv_score_DT
            max_depth_DT = max_depth
    print("The best max_depth for Decision Tree is: ", max_depth_DT)
    print("The CV score for that max_depth is: ", max_CV_DT)

    MAX_DEPTH_DT = max_depth_DT
    print("\nChoosing MAX_DEPTH =", MAX_DEPTH_DT, "\n")

    #once Max Depth is determined, train using train data to predict testing data
    X_test = X_all[:split,:]
    X_train = X_all[split:,:]
    y_test = y_all[:split]
    y_train = y_all[split:]

    #decision-tree classifier
    dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH_DT)
    dtree = dtree.fit(X_train, y_train)

    #prediction
    print("Decision-tree predictions:\n")
    predicted_labels = dtree.predict(X_test)
    answer_labels = y_test

    # print result
    s = "{0:<11} | {1:<11}".format("Predicted","Answer")
    #  arg0: left-aligned, 11 spaces, string, arg1: ditto
    print(s)
    s = "{0:<11} | {1:<11}".format("-------","-------")
    print(s)
    for p, a in zip( predicted_labels, answer_labels ):
        s = "{0:<11} | {1:<11}".format(p,a)
        print(s)

    #Calculating accuracy for category 1:
    num_count = 0
    num_correct = 0
    for num in range((len(predicted_labels))):
        if (np.equal(predicted_labels[num],np.int_(1))):
            num_count += 1
            if (np.equal(answer_labels[num],np.int_(1))):
                num_correct += 1
    correct_one = num_correct / num_count
    print("percentage of getting 1 right is:"+ str(correct_one))

    # feature importances!
    print()
    print("dtree.feature_importances_ are\n      ", dtree.feature_importances_)
    print("Order:", feature_names[0:])
    print()
    print("confidence score:")
    decision_tree_score = dtree.score(X_test, y_test, sample_weight=None)
    print(decision_tree_score)
    """
    #randomforest
    print("\n\n")
    print("     +++++ Random Forests +++++\n\n")

    X_labeled = X_all[split:,:]
    y_labeled = y_all[split:]

    #scramble data
    indices = np.random.permutation(len(X_labeled))
    X_data_full = X_labeled[indices]
    y_data_full = y_labeled[indices]
    X_train = X_data_full
    y_train = y_data_full

    #
    # cross-validation to determine the Random Forest's parameters (max_depth and n_estimators)
    #
    highest_CV_score = 0
    best_max_depth = 1
    best_number_estimator = 1

    #looping through both max_depth and num_estimator to fine the optimal pair
    for m_depth in range(1,10):
        for n_est in range(50,200,50):

            rforest = ensemble.RandomForestClassifier(max_depth=m_depth, n_estimators=n_est)
            scores = cross_val_score(rforest, X_train, y_train, cv=5)
            print("CV scores:", scores)
            print("CV scores' average:", scores.mean())
            average_cv_scores_RT = scores.mean()
            #comparison
            if (average_cv_scores_RT > highest_CV_score):
                highest_CV_score = average_cv_scores_RT
                best_max_depth = m_depth
                best_number_estimator = n_est

    print("The best pair of max_depth and n_estimators are: ", best_max_depth, "and", best_number_estimator)
    print("\nThe CV score for that pair is = ", highest_CV_score)

    # now, train the model with ALL of the training data
    X_test = X_all[:split,:]
    X_train = X_all[split:,:]
    y_test = y_all[:split]
    y_train = y_all[split:]

    # these next lines is where the full training data is used for the model
    MAX_DEPTH_RF = best_max_depth
    NUM_TREES_RF = best_number_estimator

    print()
    print("Using MAX_DEPTH=", MAX_DEPTH_RF, "and NUM_TREES=", NUM_TREES_RF)
    #randomforest classifier
    rforest = ensemble.RandomForestClassifier(max_depth=MAX_DEPTH_RF, n_estimators=NUM_TREES_RF)
    rforest = rforest.fit(X_train, y_train)

    # here are some examples, printed out:
    print("Random-forest predictions:\n")
    predicted_labels = rforest.predict(X_test)
    answer_labels = y_test

    #printing result
    s = "{0:<11} | {1:<11}".format("Predicted","Answer")
    print(s)
    s = "{0:<11} | {1:<11}".format("-------","-------")
    print(s)
    for p, a in zip( predicted_labels, answer_labels ):
        s = "{0:<11} | {1:<11}".format(p,a)
        print(s)

    #calculating accuracy for category 1
    num_count = 0
    num_correct = 0
    for num in range((len(predicted_labels))):
        if (np.equal(predicted_labels[num],np.int_(1))):
            num_count += 1
            if (np.equal(answer_labels[num],np.int_(1))):
                num_correct += 1
    correct_one = num_correct / num_count
    print("percentage of getting 1 right is:"+ str(correct_one))

    # feature importances
    print("\nrforest.feature_importances_ are\n      ", rforest.feature_importances_)
    print("Order:", feature_names[0:])
    rforest_score = rforest.score(X_test, y_test, sample_weight=None)
    print(rforest_score)
    """
    ###comparing decision tree and random forests
   # if (rforest_score >= decision_tree_score):
        #rforest = ensemble.RandomForestClassifier(max_depth=MAX_DEPTH_RF, n_estimators=NUM_TREES_RF)
        #rforest = rforest.fit(X_all, y_all)
   #     return rforest.predict(prediction_data)[0]
   # else:
        #dtree = tree.DecisionTreeClassifier(max_depth=MAX_DEPTH_DT)
        #dtree = dtree.fit(X_all, y_all)
    return dtree.predict(prediction_data)[0]

# if True:
#     randomforest("Finance", prediction_data)
