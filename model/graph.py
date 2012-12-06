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
        print "Calculating mu"
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
        print 'theta_s:\n{0}\n\n'.format(theta_s)
        print 'theta_st11:\n{0}\n\n'.format(theta_st[3])
        print 'theta_st10:\n{0}\n\n'.format(theta_st[2])
        print 'theta_st01:\n{0}\n\n'.format(theta_st[1])
        print 'theta_st00:\n{0}\n\n'.format(theta_st[0])
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
                mu_st11[0:self.num_sites,self.num_sites:] += upright[3] # nn11
                mu_st10[0:self.num_sites,self.num_sites:] += upright[2] # nn10
                mu_st01[0:self.num_sites,self.num_sites:] += upright[1] # nn01
                mu_st00[0:self.num_sites,self.num_sites:] += upright[0] # nn00
                """
                Calculate the edges from n'->n'.
                This is the lower-right quadrant.
                """
                lowright = self.calc_mu_quadrant(n2, n2)
                mu_s[0,self.num_sites:] += n2
                mu_st11[self.num_sites:,self.num_sites:] += lowright[3] # nn11
                mu_st10[self.num_sites:,self.num_sites:] += lowright[2] # nn10
                mu_st01[self.num_sites:,self.num_sites:] += lowright[1] # nn01
                mu_st00[self.num_sites:,self.num_sites:] += lowright[0] # nn00
            if total_samples > 50000:
                break
        mu_st11 = np.triu(mu_st11)
        mu_st10 = np.triu(mu_st10)
        mu_st01 = np.triu(mu_st01)
        mu_st00 = np.triu(mu_st00)
        mu_s /= total_samples
        mu_st11 /= total_samples
        mu_st10 /= total_samples
        mu_st01 /= total_samples
        mu_st00 /= total_samples
        print "Mu_s:\n{0}".format(mu_s)
        print range(3), range(3)
        print "Mu_st11:\n{0}\n\n".format(mu_st11)
        print "Mu_st10:\n{0}\n\n".format(mu_st10)
        print "Mu_st01:\n{0}\n\n".format(mu_st01)
        print "Mu_st00:\n{0}\n\n".format(mu_st00)
        print "Summed:\n{0}\n\n".format(mu_st11 + mu_st10 + mu_st01 + mu_st00)
        return [mu_s, mu_st00, mu_st01, mu_st10, mu_st11]

    def calc_mu_quadrant(self, n1, n2):
        nn11 = n1.T * n2
        np.fill_diagonal(nn11, 0)
        nn10 = n1.T * np.matrix(np.ones(n1.shape[1])) - nn11
        np.fill_diagonal(nn10, 0)
        nn01 =  n2.T * np.matrix(np.ones(n1.shape[1])) - nn11
        np.fill_diagonal(nn01, 0)
        s1 = (n1.shape[1],n1.shape[1])
        nn00 = np.matrix(np.ones(s1)) - nn11 - nn10 - nn01
        np.fill_diagonal(nn00, 0)
        return (nn00, nn01, nn10, nn11)

    def prob(self, state):
        """
        Calculates the probability of a given state using the exponential
        family parameterization learned from a prior dataset. Note that
        we are assuming A(theta) = 0 (i.e., the graph is triangulated).
        Also note the similarity to calc_mu_quadrant.
        """
        sum_s = np.sum(state * self.nodes.T)
        n1 = state[0,0:self.num_sites]
        n2 = state[0,self.num_sites:]
        mu_s = np.matrix(np.zeros((1,self.num_nodes)))
        s = np.zeros((self.num_nodes, self.num_nodes))
        mu_st11 = np.matrix(s)
        mu_st10 = np.matrix(s)
        mu_st01 = np.matrix(s)
        mu_st00 = np.matrix(s)

        """
        Calculate the edges from n->n'.
        This is the upper-right quadrant.
        """	
        upright = self.calc_mu_quadrant(n1, n2)
        mu_s[0,0:self.num_sites] += n1
        mu_st11[0:self.num_sites,self.num_sites:] += upright[3] # nn11
        mu_st10[0:self.num_sites,self.num_sites:] += upright[2] # nn10
        mu_st01[0:self.num_sites,self.num_sites:] += upright[1] # nn01
        mu_st00[0:self.num_sites,self.num_sites:] += upright[0] # nn00
        """
        Calculate the edges from n'->n'.
        This is the lower-right quadrant.
        """
        lowright = self.calc_mu_quadrant(n2, n2)
        mu_s[0,self.num_sites:] += n2
        mu_st11[self.num_sites:,self.num_sites:] += lowright[3] # nn11
        mu_st10[self.num_sites:,self.num_sites:] += lowright[2] # nn10
        mu_st01[self.num_sites:,self.num_sites:] += lowright[1] # nn01
        mu_st00[self.num_sites:,self.num_sites:] += lowright[0] # nn00

        mu_st11 = np.triu(mu_st11)
        mu_st10 = np.triu(mu_st10)
        mu_st01 = np.triu(mu_st01)
        mu_st00 = np.triu(mu_st00)

        sum_s = np.sum(mu_s.T * self.nodes)
        sum_s = np.sum(mu_s.T * -1 * (self.nodes - np.ones((1,self.num_nodes)) ) 

        sum_st00 = np.sum(np.multiply(mu_st00, self.edges[0]))
        sum_st01 = np.sum(np.multiply(mu_st01, self.edges[1]))
        sum_st10 = np.sum(np.multiply(mu_st10, self.edges[2]))
        sum_st11 = np.sum(np.multiply(mu_st11, self.edges[3]))
        result = sum_s + sum_st00 + sum_st01 + sum_st10 + sum_st11
        #print "S: {0} ST[00]: {1} ST[01]: {2} ST[10]: {3} ST[11]: {4}".format(sum_s, sum_st00, sum_st01, sum_st10, sum_st11)

        print state
        print result
        #print "Prob: {0}".format(math.exp(result))
        #return math.exp(sum_s + sum_st00 + sum_st01 + sum_st10 + sum_st11)
        #
        #pseudo-likelihood
        if result < 0.000001:
            return 0
        print math.exp(result)
        return result

    def predict(self, current_nodes):
        """
        Return the approximate MAP assignment to the next nodes given current_nodes.
        """
        return self.predict_hill_climbing(current_nodes)

    def predict_hill_climbing(self, current_nodes, steps_per_node=5):
        """
        A simple greedy hill climbing procedure to search for a MAP assignment.
        """
        steps = self.num_sites * steps_per_node
        state = np.matrix(np.zeros((1,self.num_nodes)))
        state[0,0:self.num_sites] = current_nodes
        for i in range(0,steps):
            nidx = random.randrange(self.num_sites, self.num_nodes)
            state[0,nidx] = 0
            p0 = self.prob(state)
            state[0,nidx] = 1
            p1 = self.prob(state)
            if p0 > p1:
                state[0,nidx] = 0
        print 'Final prob: {0}'.format(self.prob(state))
        return state[0,self.num_sites:]

    def test(self, test_file):
        """
        Tests the model for accuracy against a hold-out testing file.
        Returns a tuple of (# correct, # total, percent correct, percent nodes correct)
        """
        correct = 0
        total = 0
        nodewise_correct = 0
        for sample in get_samples(test_file):
            print total
            for i in range(0, sample.shape[0]-1):
                current_nodes = sample[i,0:self.num_sites]
                next = sample[i+1,0:self.num_sites]
                predicted = self.predict(current_nodes)
                true_state = np.matrix(np.zeros((self.num_nodes)))
                true_state[0,:self.num_sites] = current_nodes
                true_state[0,self.num_sites:] = next
                print "Ground: {0}".format(true_state)
                print "Ground prob: {0}".format(self.prob(true_state))
                print "Next: {0} Predicted: {1}".format(next, predicted)
                if (next == predicted).all():
                    correct += 1
                    nodewise_correct += 1
                else:
                    for j in range(0, self.num_sites):
                        if next[0,j] == predicted[0,j]:
                            nodewise_correct += 1 / float(self.num_sites)
                total += 1
        return (correct, total, correct / float(total), nodewise_correct / float(total))


if __name__ == "__main__":
    g = Graph(pickle.load(open('data/nodes.txt', 'rb')))
    g.learn_parameters('data/infections_daily.csv')