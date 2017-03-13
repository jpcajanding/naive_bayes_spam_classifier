__author__ = 'JCajandi'
#this code executes the test of the classifiers

import os
import re
import sys
import operator
import math

#test preparations#
#read labels
label_path = open(r'labels', 'r')
lambda_factor = 1.0

linesOfText = label_path.readlines()
label_path.close()
training_data_class = [[0 for x in range(300)] for y in range(71)]
testing_data_class = [[0 for x in range(301)] for y in range(127)]

for lineoftext in linesOfText:
    splittedline = lineoftext.split()
    datasplit = splittedline[1].split("/")
    if long(datasplit[2]) <= 70:
        training_data_class[long(datasplit[2])][long(datasplit[3])] = splittedline[0]
    else:
        testing_data_class[long(datasplit[2])][long(datasplit[3])] = splittedline[0]
linesOfText = None

# get dictionary
dictionary_path = open(r'dictionary_improved.txt','r')
dictionary = dictionary_path.read()
dictionary_path.close()
dictionary = dictionary.split(",")
dictionary = [word for word in dictionary if word.isalpha()]
dictionary_size = len(dictionary)
print dictionary_size

#get probability of hams and spams
num_spam = sum(files.count('spam') for files in training_data_class)
num_ham = sum(files.count('ham') for files in training_data_class)
training_files = num_spam + num_ham

probability_of_spam = math.log(float(num_spam)/ training_files)
probability_of_ham = math.log(float(num_ham)/ training_files)
print probability_of_spam
print probability_of_ham

#get classifiers
spam_words = open(r'spam_classifier_improved_lambda_factor_' + str(lambda_factor) + '.txt','r')
spam_classifiers_true = spam_words.read()
spam_words.close()
spam_classifiers_true = spam_classifiers_true.split(",")
spam_classifiers_true = [float(num) for num in filter(None, spam_classifiers_true)]
spam_classifiers_false = [1 - x for x in spam_classifiers_true]
spam_classifiers_true = [math.log(num) for num in spam_classifiers_true]
spam_classifiers_false = [math.log(num) for num in spam_classifiers_false]


ham_words = open(r'ham_classifier_improved_lambda_factor_' + str(lambda_factor) + '.txt','r')
ham_classifiers_true = ham_words.read()
ham_words.close()
ham_classifiers_true = ham_classifiers_true.split(",")
ham_classifiers_true = [float(num) for num in filter(None, ham_classifiers_true)]
ham_classifiers_false = [1 - x for x in ham_classifiers_true]
ham_classifiers_true = [math.log(num) for num in ham_classifiers_true]
ham_classifiers_false = [math.log(num) for num in ham_classifiers_false]

#define basic values --> all false
spam_classifiers_words = spam_classifiers_false
ham_classifiers_words = ham_classifiers_false

class_results = []
check_result = []
test_data_folder=71
#test#
while test_data_folder < 127:
    test_data_path = r'data'
    test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3)
    path, dirs, files = os.walk(test_data_path).next()
    file_count = len(files)
    test_data_file = 0

    while test_data_file < file_count:
        #define basic values --> all false
        spam_classifiers_words = spam_classifiers_false
        ham_classifiers_words = ham_classifiers_false

        #initialize getting the file
        test_data_path = r'data'
        test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3) + '\\' + str(test_data_file).zfill(3)
        print 'Testing folder {0}, file {1}.'.format(str(test_data_folder).zfill(3),str(test_data_file).zfill(3))
        sys.stdout.flush()

        #get the file
        test_data_path = open(test_data_path,'r')
        test_data_lines = test_data_path.readlines()

        #create a list of unique words from the file
        file_unique_words=[]
        for test_data_line in test_data_lines:
            test_data_line = re.split('\W+',test_data_line)
            test_data_line = filter(None,test_data_line) #remove empty strings
            test_data_line = [word for word in test_data_line if word.isalpha()]
            file_unique_words = (set(file_unique_words)|set(test_data_line))

        #flag words in dictionary
        for word in file_unique_words:
            #check if in dictionary
            if word in dictionary:
                word_index = dictionary.index(word)

                #set the index of word to true in both ham and spam probabilities
                spam_classifiers_words[word_index] = spam_classifiers_true[word_index]
                ham_classifiers_words[word_index] = ham_classifiers_true[word_index]

        #get the probability that email is spam
        spam_prob = sum(spam_classifiers_words) + probability_of_spam
        ham_prob = sum(ham_classifiers_words) + probability_of_ham

        #get class
        if ham_prob > spam_prob:
            result_class = 'ham'
        else:
            result_class = 'spam'

        #store results
        class_results.append(result_class + '_' + str(test_data_folder).zfill(3) + '_' + str(test_data_file).zfill(3))

        #next test_data_file
        test_data_file += 1

        if testing_data_class[test_data_folder][test_data_file] == result_class:
            check_result.append(1)
        else:
            check_result.append(0)


    test_data_folder += 1

#write results
write_results = open(r'test_results_improved2_lambda_factor_' + str(lambda_factor) + '.txt', 'w')
for result in class_results:
    write_results.write(result + ',')
write_results.close()

print sum(check_result)