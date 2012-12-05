import numpy as np
from get_samples import get_samples
import math
import pickle
import random

class Graph:
	def __init__(self, sites):
		self.num_sites = len(sites)
		self.num_nodes = len(sites) * 2
		print "initializing %s nodes" %(self.num_nodes)
		self.nodes = np.empty((self.num_nodes, 0))
		print "initializing %s^2 edges" %(self.num_nodes)
		self.edges = np.empty((4,self.num_nodes, self.num_nodes))

	def learn_parameters(self, samples):
		# returns a list: [mu_s, mu_st00, mu_st01, mu_st10, mu_st11]
	 	mu = self.calc_mu(samples)
	 	mu_s = mu[0]
	 	mu_st = mu[1:]
	 	print "Learning theta_s"
	 	theta_s = np.matrix(np.zeros((1, self.num_nodes)))
	 	for i in range(0,mu_s.shape[1]):
	 		if mu_s[0,i] > 0:
				theta_s[0,i] = math.log(mu_s[0,i])
		s = (self.num_nodes, self.num_nodes)
		theta_st = [np.matrix(np.zeros(s)),np.matrix(np.zeros(s)),np.matrix(np.zeros(s)),np.matrix(np.zeros(s))]
		denom00 = (1 - mu_s.T) * (1 - mu_s)
		denom01 = (1 - mu_s.T) * mu_s
		denom10 = mu_s.T * (1 - mu_s)
		denom11 = mu_s.T * mu_s
		denom = [denom00,denom01,denom10,denom11]
	 	print "Learning theta_st"
	 	#TODO: This could be made faster by using a numpy selector
		for k in range(0,4):
			for i in range(self.num_nodes):
				for j in range(self.num_nodes):
					if mu_st[k][i,j] > 0 and denom[k][i,j] > 0:
						theta_st[k][i,j] = math.log(mu_st[k][i,j]/denom[k][i,j])
		np.save(samples.replace('.csv', '_theta_s'), theta_s)
		np.save(samples.replace('.csv', '_theta_st'), theta_st)
		self.nodes = theta_s
		self.edges = theta_st

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

    def prob(self, state):
        """
        Calculates the probability of a given state using the exponential
        family parameterization learned from a prior dataset. Note that
        we are assuming A(theta) = 0 (i.e., the graph is triangulated).
        """
        sum_s = np.sum(state * np.transpose(self.nodes))
        
        nn11 = np.transpose(state) * state
        np.fill_diagonal(nn11, 0)
        nn10 = np.transpose(state) * np.matrix(np.ones(state.shape[1])) - nn11
        np.fill_diagonal(nn10, 0)
        nn01 = np.transpose(nn10)
        s = (state.shape[1],state.shape[1])
        nn00 = np.matrix(np.ones(s)) - nn11 - nn10 - nn01
        np.fill_diagonal(nn00, 0)

        sum_st00 = np.sum(np.multiply(nn00, self.edges[0]))
        sum_st01 = np.sum(np.multiply(nn01, self.edges[1]))
        sum_st10 = np.sum(np.multiply(nn10, self.edges[2]))
        sum_st11 = np.sum(np.multiply(nn11, self.edges[3]))
        return math.exp(sum_s + sum_st00 + sum_st01 + sum_st10 + sum_st11)

	def predict(self, current_nodes):
	 	return predict_hill_climbing(current_nodes)

    def predict_hill_climbing(self, current_nodes, steps=100):
        state = np.matrix(np.zeros(1,self.num_nodes))
        state[0,:self.num_sites] = current_nodes
        for i in range(0,steps):
            nidx = random.randrange(self.num_sites, self.num_nodes)
            state[0,nidx] = 0
            p0 = self.prob(state)
            state[0,nidx] = 1
            p1 = self.prob(state)
            if p0 > p1:
                state[0,nidx] = 1
        return state



if __name__ == "__main__":
	g = Graph(pickle.load(open('data/nodes.txt', 'rb')))
	g.learn_parameters('data/infections_daily.csv')