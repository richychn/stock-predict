import numpy as np            
import pandas as pd
import math
from sklearn import tree      
from sklearn import ensemble 
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier

def adaboost(industry,prediction_data):
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

    for i in range(len(prediction_data[0])):
        if (math.isnan(prediction_data[0][i])):
            prediction_data[0][i] = fill[i]

    print("\n+++ End of pandas +++\n")

    print("+++ Start of numpy/scikit-learn +++\n")

    print("+++++ Adaboost +++++\n\n")

    #Data needs to be in numpy arrays, converts dataframe to numpy array
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

    #
    # some labels to make the graphical trees more readable...
    #
    # print("Some labels for the graphical tree:")
    # feature_names = []
    # for i in range(1,28):
    #     feature_names.append("f"+str(i))
    # target_names = ['growth_rate']

    #initializing testing sets
    X_test = X_all[:split,:]
    y_test = y_all[:split]

    # cross-validation and scoring to determine parameter: max_depth
    highest_CV_score = 0
    best_number_estimator = 1
    for n_est in range(50,200,50):

        adb = ensemble.AdaBoostClassifier(n_estimators=n_est)
        scores = cross_val_score(adb, X_train, y_train, cv=5)
        print("CV scores:", scores)
        print("CV scores' average:", scores.mean())
        average_cv_scores_ADB = scores.mean()
        #comparison
        if (average_cv_scores_ADB > highest_CV_score):
            highest_CV_score = average_cv_scores_ADB
            best_number_estimator = n_est

    #once Max Depth is determined, train using train data to predict testing data
    X_test = X_all[:split,:]
    X_train = X_all[split:,:]
    y_test = y_all[:split]
    y_train = y_all[split:]

    # adaboost classifier
    adb = AdaBoostClassifier(n_estimators=best_number_estimator)
    adb = adb.fit(X_train, y_train)

    #prediction
    print("AdaBoost predictions:\n")
    predicted_labels = adb.predict(X_test)
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
    def accuracy_of(cat):
        num_count = 0
        num_correct = 0
        for num in range((len(predicted_labels))):
            if (np.equal(predicted_labels[num],np.int_(cat))):
                num_count += 1
                if (np.equal(answer_labels[num],np.int_(cat))):
                    num_correct += 1
        if num_count == 0:
            correct_one = 0
        else:
            correct_one = num_correct / num_count
        print("percentage of getting " + str(cat) + " right is:"+ str(correct_one))
    
    # accuracy_of(0)
    # accuracy_of(1)
    # accuracy_of(2)
    # accuracy_of(3)
    # accuracy_of(4)
    # accuracy_of(5)
    # accuracy_of(6)
    # # feature importances!
    # print()
    # print("adb.feature_importances_ are\n      ", adb.feature_importances_)
    # print("Order:", feature_names[0:])
    # print()

    # print("adb.decision_function on X_train is", adb.decision_function(X_train))

    print("confidence score:")
    adb_score = adb.score(X_test, y_test, sample_weight=None)
    print(adb_score)

    prediction = adb.predict(prediction_data)
    return adb_score, prediction

#adaboost("Technology")
#adaboost("Energy")