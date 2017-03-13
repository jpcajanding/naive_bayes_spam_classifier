__author__ = 'JCajandi'

#import nltk

from nltk import word_tokenize, WordNetLemmatizer
# from nltk import WordNetLemmatizer

ex='I am atrial'
lem=WordNetLemmatizer()
i=0
f = word_tokenize(ex)
g = [0]*3
for i in xrange(0,3):
    g[i] = i*i
i=0
# for i in f:
print lem.lemmatize(f)

print g

print f
