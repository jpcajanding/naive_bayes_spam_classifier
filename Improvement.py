__author__ = 'JCajandi'
#this code search for the best 200 words to creat a new dictionary

import os
import re
import sys
import operator
import math
import numpy

# get dictionary
dictionary_path = open(r'dictionary_clean.txt','r')
dictionary = dictionary_path.read()
dictionary_path.close()
dictionary = dictionary.split(",")
dictionary = [word for word in dictionary if word.isalpha()]
dictionary_size = len(dictionary)

spam_words = open(r'spam_word_count.txt','r')
spam_word_count = spam_words.read()
spam_words.close()
spam_word_count = spam_word_count.split(",")
spam_word_count = [int(num) for num in spam_word_count if num.isdigit()]


ham_words = open(r'ham_word_count.txt','r')
ham_word_count = ham_words.read()
ham_words.close()
ham_word_count = ham_word_count.split(",")
ham_word_count = [int(num) for num in ham_word_count if num.isdigit()]

spam_word_count = numpy.array(spam_word_count)
ham_word_count = numpy.array(ham_word_count)

spam_word_index = spam_word_count.argsort()[-(len(spam_word_count)):][::-1]
ham_word_index = ham_word_count.argsort()[-(len(ham_word_count)):][::-1]

dictionary_new = []
ham_word_count_new = []
spam_word_count_new = []

# get the first 200 frequet spam words that are not frequent ham words
for index in spam_word_index:
    if index not in ham_word_index[:200]:
        dictionary_new.append(dictionary[index])
        ham_word_count_new.append(ham_word_count[index])
        spam_word_count_new.append(spam_word_count[index])

    if len(dictionary_new) == 200: break

write_dictionary = open(r'dictionary_improved.txt', 'w')
for word in dictionary_new:
    write_dictionary.write(word + ',')
write_dictionary.close()

write_spam = open(r'spam_word_count_improved.txt', 'w')
for word in spam_word_count_new:
    write_spam.write(str(word) + ',')
write_spam.close()

write_ham = open(r'ham_word_count_improved.txt', 'w')
for word in ham_word_count_new:
    write_ham.write(str(word) + ',')
write_ham.close()

# classifiers
lambda_factors = [0.005, 0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]

#read labels
label_path = open(r'labels', 'r')

linesOfText = label_path.readlines()
label_path.close()
training_data_class = [[0 for x in range(300)] for y in range(71)]

for lineoftext in linesOfText:
    splittedline = lineoftext.split()
    datasplit=splittedline[1].split("/")
    if long(datasplit[2]) > 70:
        break
    training_data_class[long(datasplit[2])][long(datasplit[3])] = splittedline[0]
linesOfText = None

for lambda_factor in lambda_factors:
    num_spam = sum(files.count('spam') for files in training_data_class)
    num_ham = sum(files.count('ham') for files in training_data_class)

    spam_divider = num_spam + (len(dictionary_new) * lambda_factor)
    ham_divider = num_ham + (len(dictionary_new) * lambda_factor)

    #create classifiers
    spam_classifiers = [(num + lambda_factor)/spam_divider for num in spam_word_count_new]
    ham_classifiers = [(num + lambda_factor)/spam_divider for num in ham_word_count_new]

    write_spam_classifier = open(r'spam_classifier_improved_lambda_factor_' + str(lambda_factor) + '.txt', 'w')
    for num in spam_classifiers:
        write_spam_classifier.write(str(num) + ',')
    write_spam_classifier.close()

    write_ham_classifier = open(r'ham_classifier_improved_lambda_factor_' + str(lambda_factor) + '.txt', 'w')
    for num in ham_classifiers:
        write_ham_classifier.write(str(num) + ',')
    write_ham_classifier.close()


