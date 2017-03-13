__author__ = 'JCajandi'
# this is the training module for the naive bayes classifier

import os
import re
import sys
import operator

#read labels
label_path = open(r'labels', 'r')

linesOfText = label_path.readlines()
training_data_class = [[0 for x in range(300)] for y in range(71)]

for lineoftext in linesOfText:
    splittedline = lineoftext.split()
    datasplit=splittedline[1].split("/")
    if long(datasplit[2]) > 70:
        break
    training_data_class[long(datasplit[2])][long(datasplit[3])] = splittedline[0]

# get dictionary
dictionary_path = open(r'dictionary.txt','r')
dictionary = dictionary_path.read()
dictionary_path.close
dictionary = dictionary.split(",")
print len(dictionary)
dictionary = [word for word in dictionary if word.isalpha()]

# create ham and spam word counter arrays
num_spam = sum(files.count('spam') for files in training_data_class)
num_ham = sum(files.count('ham') for files in training_data_class)

spam_words = [0]*len(dictionary)
spam_word_sum = spam_words
ham_words = [0]*len(dictionary)
ham_word_sum = ham_words


# training
word_append_count = 0
test_data_folder = 0
spam_count = 0
ham_count = 0

while test_data_folder <= 70:
    test_data_path = r'data'
    test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3)
    path, dirs, files = os.walk(test_data_path).next()
    file_count = len(files)
    test_data_file = 0

    while test_data_file < file_count:
        test_data_path = r'data'
        test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3) + '\\' + str(test_data_file).zfill(3)
        print 'Training folder {0}, file {1}.'.format(str(test_data_folder).zfill(3),str(test_data_file).zfill(3))
        sys.stdout.flush()

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
            # else:
            #     dictionary.append(word)
            #     word_append_count+=1

            #check if ham or spam
                if training_data_class[test_data_folder][test_data_file] == 'spam':
                    spam_words[word_index] = 1
                else:
                    ham_words[word_index] = 1

        if training_data_class[test_data_folder][test_data_file] == 'spam':
            spam_count += 1
            spam_word_sum = [spam_word_sum[i] + spam_words[i] for i in xrange(len(spam_word_sum))]
            spam_words = [0]*len(dictionary)
        else:
            ham_count += 1
            ham_word_sum = [ham_word_sum[i] + ham_words[i] for i in xrange(len(ham_word_sum))]
            ham_words = [0]*len(dictionary)

        #next test_data_file
        test_data_file += 1

    test_data_folder += 1

write_spam = open(r'spam_word_count.txt', 'w')
for word in spam_word_sum:
    write_spam.write(str(word) + ',')
write_spam.close()

write_ham = open(r'ham_word_count.txt', 'w')
for word in ham_word_sum:
    write_ham.write(str(word) + ',')
write_ham.close()