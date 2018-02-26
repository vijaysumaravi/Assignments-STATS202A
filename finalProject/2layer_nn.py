#########################################################
## Stat 202A - Final Project
## Author: Vijay Ravi
## Date : December 13th, 2017
## Description: This script implements a two layer neural network
#########################################################

#############################################################
## INSTRUCTIONS: Please fill in the missing lines of code
## only where specified. Do not change function names,
## function inputs or outputs. You can add examples at the
## end of the script (in the "Optional examples" section) to
## double-check your work, but MAKE SURE TO COMMENT OUT ALL
## OF YOUR EXAMPLES BEFORE SUBMITTING.
##
## Very important: Do not use the function "os.chdir" anywhere
## in your code. If you do, I will be unable to grade your
## work since Python will attempt to change my working directory
## to one that does not exist.
#############################################################
import numpy as np
import csv
import random
import math
import matplotlib.pyplot as plt

def prepare_data(valid_digits=np.array((6,5))):
    if len(valid_digits)!=2:
        raise Exception("Error: you must specify exactly 2 digits for classification!")

    csvfile=open('digits.csv','r')
    reader=csv.reader(csvfile)
    data=[]
    for line in reader:
        data.append(line)

    csvfile.close()
    digits=np.asarray(data,dtype='float')

    X=digits[(digits[:,64]==valid_digits[0]) | (digits[:,64]==valid_digits[1]),0:64]
    Y = digits[(digits[:, 64] == valid_digits[0]) | (digits[:, 64] == valid_digits[1]), 64:65]

    X=np.asarray(map(lambda k: X[k,:]/X[k,:].max(), range(0,len(X))))

    Y[Y==valid_digits[0]]=0
    Y[Y==valid_digits[1]]=1

    training_set=random.sample(range(360),270)

    testing_set=list(set(range(360)).difference(set(training_set)))

    X_train=X[training_set,:]
    Y_train=Y[training_set,]

    X_test=X[testing_set,:]
    Y_test=Y[testing_set,]

    return X_train,Y_train,X_test,Y_test


def accuracy(p,y):

    acc=np.mean((p>0.5)==(y==1))
    return acc

####################################################
## Two Layer Neural Network  ##
####################################################

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
## Train a two layer neural network to classify the digits data ##
## Use Relu as the activation function for the first layer. Use Sigmoid as the activation function for the second layer##
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
def my_NN(X_train,Y_train,X_test,Y_test,num_hidden=20,num_iterations=1000,learning_rate=1e-1):

    n=X_train.shape[0]
    p=X_train.shape[1]+1
    ntest=X_test.shape[0]

    X_train1= np.concatenate((np.repeat(1,n,axis=0).reshape((n,1)),X_train),axis=1)
    X_test1 = np.concatenate((np.repeat(1, ntest, axis=0).reshape((ntest, 1)), X_test), axis=1)
    #alpha=np.random.standard_normal((p,num_hidden))
    alpha = np.random.normal(0, 0.3, (p, num_hidden))
    #beta=np.random.standard_normal((num_hidden+1,1))
    beta = np.random.normal(0, 0.3, (num_hidden+1, 1))
    acc_train=np.repeat(0.,num_iterations)
    acc_test=np.repeat(0.,num_iterations)

    #######################
    ## FILL IN CODE HERE ##
    #######################

    for it in range(num_iterations):

        Z = np.maximum(0,X_train1.dot(alpha))
        Z1 = np.concatenate((np.repeat(1, n, axis=0).reshape((n, 1)), Z), axis=1)
        pr = 1 / (1 + np.exp((-1) * Z1.dot(beta)))

        dbeta = np.reshape(np.matmul(np.ones(n), np.tile(np.subtract(Y_train, pr), (1,num_hidden+1)) / n), (num_hidden+1,1))
        beta = beta + learning_rate * dbeta

        for i in range(num_hidden):
            z_temp =  np.reshape(Z[:,i],(n,1))
            da = np.multiply(np.subtract(Y_train, pr)*beta[i+1][0], np.multiply(z_temp, (1-z_temp)))
            dalpha1 = np.ones(n)
            dalpha2 = np.tile(da,(1,p))
            dalpha = np.matrix(np.matmul(dalpha1, dalpha2))/n
            alpha[:, i] = np.reshape(np.transpose(np.matrix(alpha[:, i])) + (learning_rate * np.transpose(dalpha)),(1,p))


        acc_train[it] = accuracy(pr, Y_train)
        Ztest = np.maximum(0,X_test1.dot(alpha))
        Ztest1 = np.concatenate((np.repeat(1, ntest, axis=0).reshape((ntest, 1)), Ztest), axis=1)
        prtest = 1 / (1 + np.exp((-1) * Ztest1.dot(beta)))
        acc_test[it] = accuracy(prtest, Y_test)

        if it % 20 == 0:
            print("Iteration ", it, "Training Accuracy: ", acc_train[it], "Testing Accuracy: ", acc_test[it])



    ## Function should output 4 things:
    ## 1. The learned parameters of the first layer of the neural network, alpha
    ## 2. The learned parameters of the second layer of the neural network, beta
    ## 3. The accuracy over the training set, acc_train (a "num_iterations" dimensional vector).
    ## 4. The accuracy over the testing set, acc_test (a "num_iterations" dimensional vector).
    return alpha,beta,acc_train,acc_test


############################################################################
## Test your functions and visualize the results here##
############################################################################
X_train, Y_train, X_test, Y_test = prepare_data()
alpha,beta,acc_train,acc_test=my_NN(X_train,Y_train,X_test,Y_test,num_hidden=50,num_iterations=1000,learning_rate=0.5)
plt.axis([0,1000,0,1.5])
plt.plot(acc_train, label="Training Accuracy")
plt.plot(acc_test, label="Testing Accuracy")
plt.legend()
plt.show()
####################################################
## Optional examples (comment out your examples!) ##
####################################################




