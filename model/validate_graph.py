import numpy as np
import math
import random
import sys
from get_samples import get_samples
import graph

def test(data_file_prefix, num_sites, num_splits):
    results = []
    for fold in range(num_splits):
        print "Fold %d of %d" % (fold+1, num_splits)
        train_file = data_file_prefix + '_train' + str(fold) + '.csv'
        test_file  = data_file_prefix + '_test' + str(fold) + '.csv'
        g = graph.Graph(range(num_sites))
        print "Learning parameters..."
        g.learn_parameters(train_file)
        print "testing...."
        results.append(g.test(test_file))
        np.savez(data_file_prefix + "results.npz", results=results)
    print "all done testing!"
    pretty_print(results)

def pretty_print(results):
    print 'Fold'.center(10) + '|' + '# Correct'.center(10) + "|" + 'Total'.center(10) + "|" + '% Correct'.center(10) + "|" + '% Nodes Correct'.center(20)
    for i,r in enumerate(results):
        print '{0}|{1}|{2}|{3}|{4}'.format(str(i).center(10),str(r[0]).center(10),str(r[1]).center(10),str(r[2]).center(10),str(r[3]).center(20))

def create_holdouts(filename, num_splits):
    print "Creating testing data"
    count = 0
    splits = [open(filename.replace('.csv', '_test{0}.csv'.format(i)), 'wb') for i in range(0,num_splits)]
    for sample in get_samples(filename):
        f = splits[count % num_splits]
        for row in range(0,sample.shape[0]):
            f.write(','.join([str(x) for x in sample[row,:].tolist()[0]]))
            f.write('\n')
        f.write('\n')
        count += 1
        print count

def create_training(filename, num_splits):
    print "Creating training data"
    count = 0
    splits = [open(filename.replace('.csv', '_train{0}.csv'.format(i)), 'wb') for i in range(0,num_splits)]
    for sample in get_samples(filename):
        for i in range(0,num_splits):
            if count % num_splits == i:
                continue
            f = splits[count % num_splits]
            for row in range(0,sample.shape[0]):
                f.write(','.join([str(x) for x in sample[row,:].tolist()[0]]))
                f.write('\n')
            f.write('\n')
        count += 1
        print count

def percent_split(filename, percent, num_splits):
    print 'Creating {0} splits of {1}% each from {2}'.format(num_splits, percent * 100, filename)
    training = [open(filename.replace('.csv', '_train{0}.csv'.format(i)), 'wb') for i in range(0,num_splits)]
    testing = [open(filename.replace('.csv', '_test{0}.csv'.format(i)), 'wb') for i in range(0,num_splits)]
    count = 0
    for sample in get_samples(filename):
        for i in range(num_splits):
            if random.random() < percent:
                write_sample(sample, testing[i])
            else:
                write_sample(sample, training[i])
        count += 1
        print count

def write_sample(sample, f):
    for row in range(0,sample.shape[0]):
        f.write(','.join([str(x) for x in sample[row,:].tolist()[0]]))
        f.write('\n')
    f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        num_splits = int(sys.argv[2])
        percent = 0.01
        #create_training(filename, num_splits)
        #create_holdouts(filename, num_splits)
        percent_split(filename, percent, num_splits)
        print 'Done!'
    elif len(sys.argv) == 4:
        test(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    