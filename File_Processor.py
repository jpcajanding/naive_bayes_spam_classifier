__author__ = 'JCajandi'
#read labels

import os
import re
import sys

test_data_folder = 0

dictionary = []
while test_data_folder <= 70:
    test_data_path = r'data'
    test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3)
    path, dirs, files = os.walk(test_data_path).next()
    file_count = len(files)
    test_data_file = 0

    print 'File Count: {} '.format(str(file_count))
    sys.stdout.flush()
    while test_data_file < file_count:
        test_data_path = r'data'
        test_data_path = test_data_path + '\\' + str(test_data_folder).zfill(3) + '\\' + str(test_data_file).zfill(3)
        print 'Processing folder {0}, file {1}.'.format(str(test_data_folder).zfill(3),str(test_data_file).zfill(3))
        sys.stdout.flush()

        test_data_path = open(test_data_path,'r')
        test_data_lines = test_data_path.readlines()

        #create dictionary

        for test_data_line in test_data_lines:
            test_data_line = re.split('\W+',test_data_line)
            test_data_line = filter(None,test_data_line) #remove empty strings
            test_data_line = [word for word in test_data_line if word.isalpha()] #remove digits
            test_data_line = [word.lower() for word in test_data_line]
            dictionary = (set(dictionary)|set(test_data_line))
        test_data_lines = None
        print len(dictionary)
        sys.stdout.flush()
        test_data_file += 1

    test_data_folder += 1
print len(dictionary)
sys.stdout.flush()
write_dictionary = open(r'dictionary.txt', 'w')
for word in dictionary:
    write_dictionary.write(word + ',')
write_dictionary.close()
dictionary = None


