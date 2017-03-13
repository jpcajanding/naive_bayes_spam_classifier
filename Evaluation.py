__author__ = 'JCajandi'
#this code evaluate the resukts of the Naive Bayes Classifier Test

import os
import re
import sys
import operator
import math

#read labels
label_path = open(r'labels', 'r')
lambda_factors = [0.005, 0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
ham_tested_ham = 0 # true positive
spam_tested_spam = 0 # true negative
ham_tested_spam = 0 # false positive
spam_tested_ham = 0 # false negative

linesOfText = label_path.readlines()
label_path.close()
testing_data_class = [[0 for x in range(301)] for y in range(127)]

for lineoftext in linesOfText:
    splittedline = lineoftext.split()
    datasplit = splittedline[1].split("/")
    if long(datasplit[2]) > 70:
        testing_data_class[long(datasplit[2])][long(datasplit[3])] = splittedline[0]
linesOfText = None

for lambda_factor in lambda_factors:
    test_results_path = open(r'test_results_lambda_factor_' + str(lambda_factor) + '.txt','r')
    test_results = test_results_path.read()
    test_results_path.close()
    test_results = test_results.split(",")
    test_results = [num for num in filter(None, test_results)] #not sure if for loop needed or filter would do

    for test_result in test_results:
        test_result = test_result.split("_")
        if testing_data_class[long(test_result[1])][long(test_result[2])] == test_result[0]:
            if test_result[0] == 'spam':
                spam_tested_spam += 1
            else:
                ham_tested_ham +=1
        else:
            if test_result[0] == 'spam':
                ham_tested_spam += 1
            else:
                spam_tested_ham +=1

    precision = float(spam_tested_spam)/(spam_tested_spam + ham_tested_spam)
    recall = float(spam_tested_spam)/(spam_tested_spam + spam_tested_ham)

    print spam_tested_spam
    print ham_tested_ham
    print spam_tested_ham
    print ham_tested_spam
    print precision
    print recall

    write_results = open(r'precision_recall3.txt','a')
    write_results.write(str(precision) + '_' + str(recall) + '_' + str(lambda_factor) + ',')


