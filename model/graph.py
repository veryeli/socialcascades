import numpy as np
from get_samples import get_samples
import math


class Graph:
	def __init__(self, sites):
		self.dict = {}
		self.nodes = {}
		self.edges = {}
		self.num_sites = len(sites)
		self.num_nodes = len(sites) * 2
		self.init_dict(sites)
		self.init_nodes()
		self.init_edges()
		self.pair_indexer = {0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1)}
		self.pairs = {(0,0):self.ioo,(0,1):self.ioi,(1,0):self.iio,(1,1):self.iii}

	

	def init_dict(self, sites):
		i = 0
		for site in sites:
			self.dict[i]=site
			i += 1

	def init_nodes(self):
		print "initializing %s nodes" %(self.num_nodes)
		self.nodes = np.empty((self.num_nodes, 0))


	def init_edges(self):
		print "initializing %s^2 edges" %(self.num_nodes)
		self.edges = np.empty((4,self.num_nodes, self.num_nodes))

	def learn_parameters(self, samples):
		print "counting samples"
		self.num_samples=float(sum([sample.shape[0] -1 for sample in get_samples(samples)]))
		print self.num_samples
		print "Learning mu_s"
		mu_s       = self.calc_mu_s(samples)
		print mu_s
		print "Learning mu_st"
		mu_st      = self.calc_mu_st(samples)
		print mu_st

		print "Learning thetas"

		self.nodes = [math.log(mu) for mu in mu_s]
		print self.nodes

		print "Learning more thetas...."
		for k in range(4):
			for i in range(self.num_nodes):
				for j in range(self.num_nodes):
					print str(i) +' '+ str(j) + ' '+str(k)
					print mu_st.shape
					if mu_st[k][i][j] > 1.0 / self.num_samples:
						denom1 = mu_s[i] if self.pair_indexer[k][0] else 1 -mu_s[i]
						denom2 = mu_s[j] if self.pair_indexer[k][1] else 1-mu_s[j]
						denom = denom1 * denom2
						self.edges[k][i][j] = math.log(mu_st[k][i][j]/denom)
		print self.edges
			
			

	def calc_mu_s(self, samples):
		frequencies = np.array([self.get_frequency_count(sample) for sample in get_samples(samples)])
		frequencies2 = frequencies#[get_frequency_count(sample) for sample in samples[1:]]
		freq=np.concatenate((self.get_frequency_count(frequencies), self.get_frequency_count(frequencies2)))
		freq = np.array([item if item > 0 else .001 for item in freq])
		return freq/self.num_samples

	# def calc_mu_st(self, samples):
	# 	for sample in get_samples(samples):
	# 		nn11 = np.transpose(state) * state
	#         np.fill_diagonal(nn11, 0)
	#         nn10 = np.transpose(state) * np.matrix(np.ones(state.shape[1])) - nn11
	#         np.fill_diagonal(nn10, 0)
	#         nn01 = np.transpose(nn10)
	#         s = (state.shape[1],state.shape[1])
	#         nn00 = np.matrix(np.ones(s)) - nn11 - nn10 - nn01
	#         np.fill_diagonal(nn00, 0)

	def calc_mu_st(self, samples):
		freqs = np.array([])
		for i in range(4):
			pair = self.pair_indexer[i]
			new = self.get_mu_st_counts(samples, pair)/self.num_samples
			if freqs.shape[0]<1:
				freqs = new
			else:
				freqs = np.concatenate((freqs, new))
		return freqs


	def get_mu_st_counts(self, samples, pair):
		print "For pair " + str(pair)
		f = self.pairs[pair]
		counts = np.empty((self.num_nodes, self.num_nodes))
		for sample in get_samples(samples):	
			for i in range(sample.shape[0]-1):
				vec = np.concatenate((sample[i], sample[i+1]))
				for j in range(self.num_nodes):
					counts[j] += f(vec[j], vec)
		
		return np.array([counts])



	def get_frequency_count(self, sample):
		return sum([sample[i] for i in range(sample.shape[0])])

	def I(self, node1, node2, v1, v2):
		return 1 * (node1 == v1 and node2 == v2)

	def ioo(self, val, arr):
		return np.array([1 if a + val == 0 else 0 for a in arr])

	def iio(self, val, arr):
		return np.array([1 if a - val == 1 else 0 for a in arr])

	def ioi(self, val, arr):
		return np.array([1 if val - a == 1 else 0 for a in arr])

	def iii(self, val, arr):
		return np.array([1 if a + val == 2 else 0 for a in arr])


