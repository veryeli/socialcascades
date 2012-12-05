import numpy as np
from get_samples import get_samples
import math
import pickle


class Graph:
	def __init__(self, sites):
		self.num_sites = len(sites)
		self.num_nodes = len(sites) * 2
		print "initializing %s nodes" %(self.num_nodes)
		self.nodes = np.empty((self.num_nodes, 0))
		print "initializing %s^2 edges" %(self.num_nodes)
		self.edges = np.empty((4,self.num_nodes, self.num_nodes))
		#self.pair_indexer = {0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1)}
		#self.pairs = {(0,0):self.ioo,(0,1):self.ioi,(1,0):self.iio,(1,1):self.iii}

	def learn_parameters(self, samples):
		
	 	# returns a list: [mu_s, mu_st00, mu_st01, mu_st10, mu_st11]
	 	mu = self.calc_mu(samples)
	 	mu_s = mu[0]
	 	mu_st = mu[1:]
	# 	mu_s       = self.calc_mu_s(samples)
	# 	print mu_s
	# 	print "Learning mu_st"
	# 	mu_st      = self.calc_mu_st(samples)
	# 	print mu_st

	 	print "Learning theta_s"
	 	theta_s = np.matrix(np.zeros((1, self.num_nodes)))
	 	for i in range(0,mu_s.shape[1]):
	 		if mu_s[0,i] > 0:
				theta_s[0,i] = math.log(mu_s[0,i])
		
		

		s = (self.num_nodes, self.num_nodes)
		theta_st = [np.matrix(np.zeros(s)),np.matrix(np.zeros(s)),np.matrix(np.zeros(s)),np.matrix(np.zeros(s))]

		# print "counting samples"
		# self.num_samples=float(sum([sample.shape[0] -1 for sample in get_samples(samples)]))
		# print "Num Examples: %s" %(sum([1 for sample in get_samples(samples)]))
		# print "Total samples: {0}".format(self.num_samples)

		denom00 = (1 - mu_s.T) * (1 - mu_s)
		denom01 = (1 - mu_s.T) * mu_s
		denom10 = mu_s.T * (1 - mu_s)
		denom11 = mu_s.T * mu_s
		denom = [denom00,denom01,denom10,denom11]

	 	print "Learning theta_st"
		for k in range(0,4):
			for i in range(self.num_nodes):
				for j in range(self.num_nodes):
					if mu_st[k][i,j] > 0 and denom[k][i,j] > 0:
						theta_st[k][i,j] = math.log(mu_st[k][i,j]/denom[k][i,j])
						# denom1 = mu_s[i] if self.pair_indexer[k][0] else 1 -mu_s[i]
						# denom2 = mu_s[j] if self.pair_indexer[k][1] else 1-mu_s[j]
						# denom = denom1 * denom2
						# self.edges[k][i][j] = math.log(mu_st[k][i][j]/denom)
		np.save(samples.replace('.csv', '_theta_s'), theta_s)
		np.save(samples.replace('.csv', '_theta_st'), theta_st)
		self.nodes = theta_s
		self.edges = theta_st
			

	# def calc_mu_s(self, samples):
	# 	frequencies = np.array([self.get_frequency_count(sample) for sample in get_samples(samples)])
	# 	frequencies2 = frequencies#[get_frequency_count(sample) for sample in samples[1:]]
	# 	freq=np.concatenate((self.get_frequency_count(frequencies), self.get_frequency_count(frequencies2)))
	# 	freq = np.array([item if item > 0 else .001 for item in freq])
	# 	return freq/self.num_samples

	def calc_mu(self, samples):
		mu_s = np.matrix(np.zeros((1,self.num_nodes)))
		s = np.zeros((self.num_nodes, self.num_nodes))
		mu_st11 = np.matrix(s)
		mu_st10 = np.matrix(s)
		mu_st01 = np.matrix(s)
		mu_st00 = np.matrix(s)
		total_samples = 0
		for m1 in get_samples(samples):
			m2 = np.roll(m1, -1, axis=0)
			total_samples += m1.shape[0]-1
			print total_samples
			for i in range(0,m1.shape[0]-1):
				"""
				Calculate the edges from n->n'.
				This is the upper-right quadrant.
				"""
				n1 = m1[i]
				n2 = m2[i]
				upright = self.calc_mu_quadrant(n1, n2)
				mu_s[0,0:self.num_sites] += n1
				mu_st11[0:self.num_sites,self.num_sites:] += upright[0] # nn11
				mu_st10[0:self.num_sites,self.num_sites:] += upright[1] # nn10
				mu_st01[0:self.num_sites,self.num_sites:] += upright[2] # nn01
				mu_st00[0:self.num_sites,self.num_sites:] += upright[3] # nn00
				"""
				Calculate the edges from n'->n'.
				This is the lower-right quadrant.
				"""
				lowright = self.calc_mu_quadrant(n2, n2)
				mu_s[0,self.num_sites:] += n2
				mu_st11[self.num_sites:,self.num_sites:] += lowright[0] # nn11
				mu_st10[self.num_sites:,self.num_sites:] += lowright[1] # nn10
				mu_st01[self.num_sites:,self.num_sites:] += lowright[2] # nn01
				mu_st00[self.num_sites:,self.num_sites:] += lowright[3] # nn00
		mu_s /= total_samples
		mu_st11 /= total_samples
		mu_st10 /= total_samples
		mu_st01 /= total_samples
		mu_st00 /= total_samples
		print "Mu_s:\n{0}".format(mu_s)
		print "Mu_st11:\n{0}".format(mu_st11)
		return [mu_s, mu_st00, mu_st01, mu_st10, mu_st11]

	def calc_mu_quadrant(self, n1, n2):
		nn11 = n1.T * n2
		#n11 = nn11.diagonal()
		np.fill_diagonal(nn11, 0)
		nn10 = n1.T * np.matrix(np.ones(n1.shape[1])) - nn11
		np.fill_diagonal(nn10, 0)
		nn01 = nn10.T
		s1 = (n1.shape[1],n1.shape[1])
		nn00 = np.matrix(np.ones(s1)) - nn11 - nn10 - nn01
		np.fill_diagonal(nn00, 0)
		return (nn00, nn01, nn10, nn11)
	# def calc_mu_st(self, samples):
	# 	freqs = np.array([])
	# 	for i in range(4):
	# 		pair = self.pair_indexer[i]
	# 		new = self.get_mu_st_counts(samples, pair)/self.num_samples
	# 		if freqs.shape[0]<1:
	# 			freqs = new
	# 		else:
	# 			freqs = np.concatenate((freqs, new))
	# 	return freqs


	# def get_mu_st_counts(self, samples, pair):
	# 	print "For pair " + str(pair)
	# 	f = self.pairs[pair]
	# 	counts = np.empty((self.num_nodes, self.num_nodes))
	# 	for sample in get_samples(samples):	
	# 		for i in range(sample.shape[0]-1):
	# 			vec = np.concatenate((sample[i], sample[i+1]))
	# 			for j in range(self.num_nodes):
	# 				counts[j] += f(vec[j], vec)
		
	# 	return np.array([counts])

	# def predict(self, example):
	# 	pass



	# def get_frequency_count(self, sample):
	# 	return sum([sample[i] for i in range(sample.shape[0])])

	# def I(self, node1, node2, v1, v2):
	# 	return 1 * (node1 == v1 and node2 == v2)

	# def ioo(self, val, arr):
	# 	return np.array([1 if a + val == 0 else 0 for a in arr])

	# def iio(self, val, arr):
	# 	return np.array([1 if a - val == 1 else 0 for a in arr])

	# def ioi(self, val, arr):
	# 	return np.array([1 if val - a == 1 else 0 for a in arr])

	# def iii(self, val, arr):
	# 	return np.array([1 if a + val == 2 else 0 for a in arr])


if __name__ == "__main__":
	g = Graph(pickle.load(open('data/nodes.txt', 'rb')))
	g.learn_parameters('data/infections_daily.csv')