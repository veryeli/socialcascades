import numpy as np
import math
import random
import sys
from get_samples import get_samples

def test(data_file_prefix, num_sites):
    results = []
    for fold in range(6):
        print "Fold %d of 6" % (fold)
        train_file = data_file_prefix + 'train' + str(fold) + '.csv'
        test_file  = data_file_prefix + 'test' + str(fold) + '.csv'
        g = graph.Graph(range(num_sites))
        print "Learning parameters..."
        g.learn_parameters(train_file)
        print "testing...."
        results.append(g.test(test_file))
        numpy.savez(data_file_prefix + "results.npz", results=results)
    print "all done testing!"
    print results

def 

def create_holdouts(filename, num_splits):
    print "Creating testing data"
    count = 0
    splits = [open(filename.replace('.csv', '_test{0}.csv'.format(i)), 'wb') for i in range(0,num_splits)]
    for sample in get_samples(filename):
        f = splits[count % num_splits]
        for row in range(0,sample.shape[0]):
            f.write(','.join([str(x) for x in sample[row,:].tolist()[0]]))
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
        count += 1
        print count

if __name__ == "__main__":
    filename = sys.argv[1]
    num_splits = int(sys.argv[2])
    create_training(filename, num_splits)
    create_holdouts(filename, num_splits)
    print 'Done!'
    