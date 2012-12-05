import numpy as np
import math
import random
import sys

"""
Models an infection as an exponential family.
p(x|theta) = exp(sum(theta_s * x_s) + sum(theta_st * x_s * x_t) - A(theta))
"""
class InfectionModel(object):
    def __init__(self, nodes, theta_s, theta_st, a_theta = None):
        self.nodes = nodes
        self.theta_s = theta_s
        self.theta_st = theta_st
        self.a_theta = a_theta
        self.st_partial = np.ones((len(self.nodes)))
        if a_theta == None:
            self.a_theta = math.log(self.atheta_helper(0, np.matrix([0 for x in nodes.tolist()[0]])))

    def atheta_helper(self, idx, state):
        if idx == state.shape[1]:
            return self.pseudo_likelihood(state)
        state[0,idx] = 0
        val = self.atheta_helper(idx+1, state)
        state[0,idx] = 1
        return val + self.atheta_helper(idx+1, state)

    def pseudo_likelihood(self, state, z=0):
        sum_s = np.sum(state * np.transpose(self.theta_s))
        
        nn11 = np.transpose(state) * state
        np.fill_diagonal(nn11, 0)
        nn10 = np.transpose(state) * np.matrix(np.ones(state.shape[1])) - nn11
        np.fill_diagonal(nn10, 0)
        nn01 = np.transpose(nn10)
        s = (state.shape[1],state.shape[1])
        nn00 = np.matrix(np.ones(s)) - nn11 - nn10 - nn01
        np.fill_diagonal(nn00, 0)

        sum_st00 = np.sum(np.multiply(nn00, self.theta_st[0]))
        sum_st01 = np.sum(np.multiply(nn01, self.theta_st[1]))
        sum_st10 = np.sum(np.multiply(nn10, self.theta_st[2]))
        sum_st11 = np.sum(np.multiply(nn11, self.theta_st[3]))
        return math.exp(sum_s + sum_st00 + sum_st01 + sum_st10 + sum_st11 - z)

    def prob(self, state):
        p = self.pseudo_likelihood(state, self.a_theta)
        assert(p >= 0)
        assert(p <= 1)
        return p

    def gibbs(self, steps):
        for step in range(0,steps):
            nidx = (step % (self.nodes.shape[1]/2)) + (self.nodes.shape[1]/2)
            self.nodes[0,nidx] = 1
            p1 = self.prob(self.nodes)
            assert(p1 >= 0)
            assert(p1 <= 1)
            self.nodes[0,nidx] = 0
            p0 = self.prob(self.nodes)
            assert(p0 >= 0)
            assert(p0 <= 1)
            p = p1 / (p1 + p0)
            assert(p >= 0)
            assert(p <= 1)
            if random.random() < p:
                self.nodes[0,nidx] = 1

    def rmse(self, model):
        assert(self.nodes.shape == model.nodes.shape)
        return math.sqrt(self.rmse_helper(model, 0, np.matrix([0 for x in self.nodes.tolist()[0]])) / (2**self.nodes.shape[1]))

    def rmse_helper(self, model, idx, state):
        if idx == self.nodes.shape[1]:
            p0 = self.prob(state)
            p1 = model.prob(state)
            print 'Real: {0} Predicted: {1}'.format(p0, p1)
            return (p0-p1) * (p0-p1)
        state[0,idx] = 0
        val = self.rmse_helper(model, idx+1, state)
        state[0,idx] = 1
        return val + self.rmse_helper(model, idx+1, state)



def fake_samples(num_hosts, num_infections, samples_per_infection):
    num_nodes = 2*num_hosts
    nodes = np.matrix([0 for i in range(0,num_nodes)])
    theta_s = np.matrix([random.random() for x in range(0,num_nodes)])
    theta_st = np.matrix(np.zeros((num_nodes, num_nodes)))
    # Initialize edges from t->t' nodes
    for i in range(0, num_hosts):
        for j in range(num_hosts, 2*num_hosts):
            theta_st[i,j] = random.random() - 0.5
    # Initialize edges from t'->t'\i nodes
    for j in range(num_hosts, 2*num_hosts):
        for k in range(j+1, 2*num_hosts):
            theta_st[j,k] = random.random() - 0.5 # allow for some dampening nodes
    # Build our graphical model
    model = InfectionModel(nodes, theta_s, theta_st)
    np.save('data/synthetic_{0}_theta_s'.format(num_hosts), theta_s)
    np.save('data/synthetic_{0}_theta_st'.format(num_hosts), theta_st)
    np.save('data/synthetic_{0}_a_theta'.format(num_hosts), model.a_theta)
    # Generate synthetic infections
    with open('data/synthetic_{0}.csv'.format(num_hosts), 'wb') as f:
        for infection in range(0, num_infections):
            print "Infection #{0}".format(infection)
            for x in range(0, num_nodes):
                model.nodes[0,x] = 0
            #initialize nodes to 20% infection
            for x in random.sample(range(0, num_hosts), int(num_hosts/5)):
                model.nodes[0,x] = 1
            f.write(','.join(str(i) for i in model.nodes.tolist()[0][0:num_hosts]) + '\n')
            f.write(','.join(str(i) for i in model.nodes.tolist()[0][num_hosts:]) + '\n')
            for sidx in range(0, samples_per_infection):
                # generate a likely next state
                model.gibbs(num_hosts)
                # save the state as an observation
                f.write(','.join(str(i) for i in model.nodes.tolist()[0][num_hosts:]) + '\n')
                # step the model forward
                for nidx in range(0,num_hosts):
                    model.nodes[0,nidx] = model.nodes[0,nidx + num_hosts]
            f.write('\n')
            f.flush()

def zero_theta_st(theta_st):
    num_hosts = theta_st.shape[1] / 2
    num_nodes = theta_st.shape[1]
    zero = np.matrix(np.zeros((num_nodes, num_nodes)))
    for i in range(0, num_hosts):
        for j in range(num_hosts, 2*num_hosts):
            zero[i,j] = 1
    # Initialize edges from t'->t'\i nodes
    for j in range(num_hosts, 2*num_hosts):
        for k in range(j+1, 2*num_hosts):
            zero[j,k] = 1
    return np.multiply(zero,theta_st)

def compare_models():
    print 'Loading models for comparison'
    theta_s1 = np.load(sys.argv[1])
    theta_st1 = np.load(sys.argv[2])
    a_theta1 = np.load(sys.argv[3])
    theta_s2 = np.load(sys.argv[4])
    theta_st2 = np.load(sys.argv[5])
    if len(sys.argv) > 6:
        a_theta2 = np.load(sys.argv[6])
    else:
        a_theta2 = 0
    print 'Calculating RMSE'
    num_hosts = theta_s1.shape[1] / 2
    num_nodes = 2*num_hosts
    nodes = np.matrix([0 for i in range(0,num_nodes)])
    model1 = InfectionModel(nodes, theta_s1, theta_st1, a_theta1)
    model2 = InfectionModel(nodes, theta_s2, theta_st2, a_theta2)
    rmse = model1.rmse(model2)
    print 'RMSE: {0}'.format(rmse)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        fake_samples(int(sys.argv[1]),100,100)
    elif len(sys.argv) > 5:
        compare_models()

























