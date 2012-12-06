import graph
import numpy 
from get_samples import get_train_samples

def test(graph, testfile, steps):
	accuracy = []
	#we're going to look for accuracy 1, 2, ... ,steps timesteps out
	num_examples = 0
	for example in get_train_samples(test_file, steps):
		accuracy.append(graph.predict(example, steps))
	return get_stats(accuracy)

def get_stats(accuracy):
	num_trials = len(accuracy)
	pair_indexer = {0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1)}
	pairs = {(0,0):self.ioo,(0,1):self.ioi,(1,0):self.iio,(1,1):self.iii}
