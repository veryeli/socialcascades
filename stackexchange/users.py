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

class Models(object):
    def __init__(self, users, posts, site_names, stepsize=1, start_year = 2007, start_month = 1, split_ngrams = 100, ngram_min_occurs = 10):
        assert(len(posts) == len(site_names))
        assert(len(users) == len(posts))
        self.users = users
        self.posts = posts
        self.site_names = site_names
        self.split_ngrams = split_ngrams
        self.ngram_min_occurs = ngram_min_occurs
        self.stepsize = stepsize
        self.start_year = start_year
        self.start_month = start_month

    def process_all(self):
        self.create_ids()
        self.create_adjacency_matrix()
        self.split()
        #self.split_tags()

    def create_ids(self):
        self.site_ids = dict((v,i) for i,v in enumerate(self.site_names))
        self.parsers = [Pradeep(users[i], posts[i], name, i, self.split_ngrams, self.ngram_min_occurs) for i,name in enumerate(self.site_names)]
        pickle.dump(self.site_ids, open('data/site_ids.data', "wb"))
        return self.site_ids

    def create_adjacency_matrix(self):
        self.adj_matrix = np.zeros((len(self.site_names), len(self.site_names)))
        user_ids = [parser.userlist() for parser in self.parsers]
        for i in range(0,len(user_ids)):
            for j in range(0,len(user_ids)):
                if i == j:
                    self.adj_matrix[i,j] = len(user_ids[i])
                    continue
                self.adj_matrix[i,j] = len(user_ids[i] & user_ids[j])
        pickle.dump(self.adj_matrix, open('data/adj_matrix.data', "wb"))
        return self.adj_matrix

    def split(self):
        for parser in self.parsers:
            parser.split_proper(self.stepsize, self.start_year, self.start_month)
        self.clean_splits('data/ngrams/')

    def split_tags(self):
        for parser in self.parsers:
            parser.split_tags(self.stepsize)
        self.clean_splits('data/tags/')

    def clean_splits(self, base_dir):
        for ngram_file in os.listdir(base_dir):
            if ngram_file.startswith('.'):
                continue
            ngrams = pickle.load(open(base_dir + ngram_file, "rb"))
            if max([len(x) for x in ngrams.values()]) == 0:
                os.remove(base_dir + ngram_file)
        print 'Finished splitting files.'





class Pradeep(object):
    
    def __init__(self, users, posts, site_name, site_id, split_ngrams = 100, ngram_min_occurs = 10):
        self.users = users
        self.posts = posts
        self.site_name = site_name
        self.site_id = site_id
        self.split_ngrams = split_ngrams
        self.ngram_min_occurs = ngram_min_occurs

    def userlist(self):
        print 'Starting parse of {0}'.format(self.users)
        context = ET.iterparse(self.users, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        user_ids = []
        print 'Gathering user IDs'
        for event, elem in context:
            if event == "end" and elem.tag == "row":
                user_ids.append(elem.attrib['Id'])
                root.clear()
        return set(user_ids)

    def split(self, stepsize=1, start_year = 2007, start_month = 1):
        """
        A broken split that saves on memory by skipping out-of-order posts
        """
        print 'Starting parse of {0}'.format(self.posts)
        context = ET.iterparse(self.posts, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        ngrams = []
        start = datetime.datetime(start_year, start_month, 1)
        end = start + relativedelta(months = stepsize)
        print start
        for event, elem in context:
            if event == "end" and elem.tag == "row":
                text = ''.join(BeautifulSoup(elem.attrib['Body']).findAll(text=True))
                date = dateutil.parser.parse(elem.attrib['CreationDate'])
                print '\t{0}'.format(date)
                while date > end:
                    print 'Calculating collocations'
                    collocations = Pradeep.collocations_from_tokens(ngrams, self.split_ngrams, self.ngram_min_occurs)
                    print 'Saving results'
                    self.save_ngrams(collocations, start)
                    start = end
                    print start
                    end = start + relativedelta(months = stepsize)
                    ngrams = []
                if date < start:
                    continue
                bigrams = Pradeep.bigrams(text)
                for bigram in bigrams:
                    ngrams.append(bigram)
                root.clear()

    def split_proper(self, stepsize=1, start_year = 2007, start_month = 1):
        """
        A split method that holds all text in memory until the end.
        """
        print 'Starting parse of {0}'.format(self.posts)
        context = ET.iterparse(self.posts, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        ngrams = [[] for x in range(self.split_idx(start_year, start_month, datetime.datetime(2012, 1, 1)))]
        for event, elem in context:
            if event == "end" and elem.tag == "row":
                text = ''.join(BeautifulSoup(elem.attrib['Body']).findAll(text=True))
                date = dateutil.parser.parse(elem.attrib['CreationDate'])
                sidx = self.split_idx(start_year, start_month, date)
                print '\t{0}\tsidx:{1}'.format(date, sidx)
                bigrams = Pradeep.bigrams(text)
                for bigram in bigrams:
                    ngrams[sidx].append(bigram)
                root.clear()
        
        print 'Finished collecting n-grams. Processing...'
        for i,n in enumerate(ngrams):
            date = self.idx_to_date(start_year, start_month, i)
            print '{0}/{1}'.format(date.month, date.year)
            if len(n) == 0:
                print 'No elements. Skipping...'
                continue
            print '{0} items'.format(len(n))
            print '\tCalculating collocations'
            collocations = Pradeep.collocations_from_tokens(n, self.split_ngrams, self.ngram_min_occurs)
            print '\tSaving results'
            self.save_ngrams(collocations, date)
        ngrams = None

    def split_idx(self, start_year, start_month, date):
        return (date.year - start_year)*12 + start_month - date.month

    def idx_to_date(self, start_year, start_month, idx):
        print "idx: {0} yr: {1} month: {2}".format(idx, start_year + (idx + start_month) / 12, start_month + (idx % 12))
        return datetime.datetime(start_year + (idx + start_month) / 12, start_month + (idx % 12), 1)

    def split_tags(self, stepsize=1):
        print 'Starting parse of {0}'.format(self.posts)
        context = ET.iterparse(self.posts, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        # initialize tags
        tags = []
        for i in range(0,6):
            tags.append([])
            for j in range(0,12):
                tags[i].append({})
        for event, elem in context:
            if event == "end" and elem.tag == "row":
                if elem.attrib['PostTypeId'] != '1':
                    root.clear()
                    continue
                date = dateutil.parser.parse(elem.attrib['CreationDate'])
                print '\t{0}'.format(date)
                text = ''.join(BeautifulSoup(elem.attrib['Tags']).findAll(text=True))
                tokenizer = nltk.tokenize.RegexpTokenizer('[\da-zA-Z\-]+')
                tokens = tokenizer.tokenize(text.encode('ascii', 'ignore').lower())
                year = date.year - 2007
                month = date.month - 1
                for tag in tokens:
                    if not tag in tags[year][month]:
                        tags[year][month][tag] = 0
                    val = tags[year][month][tag]
                    if val is None:
                        val = 0
                    tags[year][month][tag] = val + 1
                root.clear()
        for i in range(0,5):
            for j in range(0,11):
                self.save_tags(tags[i][j], datetime.datetime(2007+i, 1+j, 1))

    def timestep(self, start, end):
        context = ET.iterparse(self.posts, events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        ngrams = []

        for event, elem in context:
            if event == "end" and elem.tag == "row":
                text = ''.join(BeautifulSoup(elem.attrib['Body']).findAll(text=True))
                date = dateutil.parser.parse(elem.attrib['CreationDate'])
                if date >= start and date <= end:
                    print date
                    bigrams = Pradeep.bigrams(text)
                    for bigram in bigrams:
                        ngrams.append(bigram)
                root.clear()
        return Pradeep.collocations_from_tokens(ngrams, self.split_ngrams, self.ngram_min_occurs)

    def save_ngrams(self, ngrams, date):
        filename = 'data/ngrams/' + str(date.year) + "_" + str(date.month) + ".ngrams"
        if not os.path.exists(filename):
            all_ngrams = {}
            pickle.dump(all_ngrams, open(filename, "wb"))
        all_ngrams = pickle.load(open(filename, "rb"))
        all_ngrams[self.site_id] = ngrams
        pickle.dump(all_ngrams, open(filename, "wb"))

    def save_tags(self, tags, date):
        filename = 'data/tags/' + str(date.year) + "_" + str(date.month) + ".tags"
        if not os.path.exists(filename):
            all_tags = {}
            pickle.dump(all_tags, open(filename, "wb"))
        all_tags = pickle.load(open(filename, "rb"))
        all_tags[self.site_id] = tags
        pickle.dump(all_tags, open(filename, "wb"))

    @staticmethod
    def bigrams(text):
        tokenizer = nltk.tokenize.RegexpTokenizer('\w+|\$[\d\.]+|[\da-zA-Z]+')
        tokens = tokenizer.tokenize(text.encode('ascii', 'ignore').lower())
        grams = nltk.bigrams(tokens)
        return grams

    @staticmethod
    def collocations_from_text(text, max_bigrams=1000, min_occur=10):
        tokenizer = nltk.tokenize.RegexpTokenizer('\w+|\$[\d\.]+|[\d\S]+')
        tokens = tokenizer.tokenize(text.encode('ascii', 'ignore').lower())
        return collocations_from_tokens(tokens, max_bigrams, min_occur)

    @staticmethod
    def collocations_from_tokens(tokens, max_bigrams=1000, min_occur=10):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = nltk.BigramCollocationFinder.from_words(tokens)
        if min_occur > 0:
            finder.apply_freq_filter(min_occur)
        return sorted(finder.nbest(bigram_measures.pmi, max_bigrams))

if __name__ == "__main__":
    site_names = [x.replace(".xml","") for x in os.listdir('data/users') if not x.startswith('.')]
    print 'Sites:'
    print site_names
    users = ['data/users/' + x + '.xml' for x in site_names]
    posts = ['data/posts/' + x + '.xml' for x in site_names]
    stepsize=1
    start_year = 2007
    start_month = 1
    split_ngrams = 1000
    ngram_min_occurs = 3
    models = Models(users, posts, site_names, stepsize, start_year, start_month, split_ngrams, ngram_min_occurs)
    models.process_all()


