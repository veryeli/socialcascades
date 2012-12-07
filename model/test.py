import sys
import os
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import nltk
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import pickle
import numpy as np
import operator
from get_samples import get_samples

def create_counts(filename):
    data = pickle.load(open(f,'rb'))
    counts = {}
    for site in data.keys():
        for bigram in data[site]:
            if not bigram in counts:
                counts[bigram] = 0
            counts[bigram] += 1
    #Debug
    sorted_bigrams = sorted(counts.iteritems(), key=operator.itemgetter(1))
    for i in range(50):
        print '{0}: {1}'.format(sorted_bigrams[i], counts[sorted_bigrams[i]])
    return counts


# site_ids = pickle.load(open('data/site_ids.data', "rb"))
# files = [x for x in os.listdir('data/users') if not x.startswith('.')]
# for f in files:
#     data = pickle.load(open(f,'rb'))
#     print '{0}: {1} sites'.format(f, len(data))

# create_counts('data/ngrams/2010_11.ngrams')

if __name__ == "__main__":
    total = 0
    print 'here'
    for sample in get_samples('data/infections_daily_test4.csv'):
        total += sample.shape[0] - 1
        print total