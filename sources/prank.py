from data_clean import generate_matrix
import numpy as np
import pandas as pd
import math
from sklearn.metrics import mean_squared_error
from math import sqrt


'''L: number of iterations'''
'''k: number of labels, in this project k = 11'''
def prank(L, k, X, y):
    (n, d) = X.shape
    if n < k:
        raise Exception("number of samples should be at least number of labels")
    theta = np.zeros((d,1), dtype = float)
    b = np.zeros((k-1, 1), dtype = float)
    S = np.zeros((n, k-1), dtype = int)
    
    '''generate label array'''
    for l in range(k-1):
        b[l, 0] = l/2
    
    '''compute label matrix of X'''
    for t in range(n):
        for l in range(k-1):
            S[t, l] = -1 if y[t, 0] <= b[l, 0] else 1
    
    '''compute theta and b(thresholds for each classifier)'''
    for iter in range(L):
        for t in range(n):
            E = np.array([])
            for l in range(k-1):
                if S[t, l] * (np.dot(X[t, :], theta) - b[l ,0]) <= 0:
                    E = np.append(E, l)
            E = E.astype(int)
            if E.size:
                for i in range(E.size):
                    l = E[i]
                    theta += S[t, l] * np.array([X[t, :]]).T
                    b[l, 0] -= S[t, l]
    return theta, b
    

def get_mean_of_all(X):
    return X[:, -3].mean()


def predict(X, k, theta, b, mean_of_all):
    result = []
    for each in range(X.shape[0]):
        #movie_ave and user_ave both exist
        if X[each, -3] and X[each, -2]:
            label = 5
            for l in range(k-1):
                if np.dot(X[each, :], theta) <= b[l, 0]:
                    label = l/2
                    break
        #lack user_ave, use movie_ave as its label
        elif X[each, -3]:
            label = X[each, -3]
        #lack movie_ave, use user_ave as its label
        elif X[each, -2]:
            laebl = X[each, -2]
        #else, use average labels of all movies in training set
        else:
            laebl = mean_of_all
        #change label to multiple of 0.5
        if not isinstance(2*label, int):
            label = int(round(2*label))/2
        result.append([label])
    return np.asarray(result)


def get_RMSE(y_actual, y_predicted):
    return sqrt(mean_squared_error(y_actual, y_predicted))


def get_MAE(y_actual, y_predicted):
    return np.sum(np.absolute(y_actual - y_predicted))/y_actual.shape[0]


def get_spec_sens_prec_accu(y_actual, y_predicted):
    label = 0
    count = 0
    spec = 0
    sens = 0
    prec = 0
    accu = 0
    while label <= 5:
        tp, tn, fp, fn = 0, 0, 0, 0
        for each in range(y_actual.shape[0]):
            if y_actual[each] == label:
                if y_predicted[each] == label:
                    tp += 1
                else:
                    fn += 1
            else:
                if y_predicted[each] == label:
                    fp += 1
                else:
                    tn += 1
        if tp+fn == 0:  #there's no label 0 in test set
            sens += 1
        else:
            sens += tp/(tp+fn)  #sensitivity
        
        if tn+fp == 0:
            spec += 1
        else:
            spec += tn/(tn+fp)      #specificity
        
        if tp+fp == 0:
            prec += 1
        else:
            prec += tp/(tp+fp)      #precision
        
        accu += (tp+tn)/(tp+fp+tn+fn)  #accuracy
        label += 0.5
        count += 1
    return spec/count, sens/count, prec/count, accu/count


def kfoldcv(X, y, k, L_array, file_movies):
    opt_L = 0
    opt_RMSE = float('inf')
    for L in L_array:
        n = X.shape[0]
        ave_RMSE = 0
        for i in range(1, k+1):
            T = np.array([])  #T as test set
            S = np.array([])  #S as train set
            for j in range(math.floor(n*(i-1)/k), math.floor(n*i/k)):
                T = np.append(T, [j])
            for j in range(n):
                S = np.append(S, [j])
            S = np.setdiff1d(S, T)
            T = T.astype(int)
            S = S.astype(int)
            #print(S)

            X_train = pd.DataFrame(X[S, :])
            y_train = pd.DataFrame(y[S])
            X_vali = pd.DataFrame(X[T, :])
            y_vali = pd.DataFrame(y[T])
            X_train, X_vali, y_train, y_vali = generate_matrix(X_train, X_vali, y_train, y_vali, file_movies)

            theta, b = prank(L, 11, X_train, y_train)
            mean_of_all = get_mean_of_all(X_train) 
            y_predicted = predict(X_vali, 11, theta, b, mean_of_all)
            ave_RMSE += get_RMSE(y_vali, y_predicted)/k
        print('average RMSE of prank with L =', L, ':')
        print(ave_RMSE)
        if ave_RMSE < opt_RMSE:
            opt_RMSE = ave_RMSE
            opt_L = L
    return opt_L



