import numpy as np

def learn_params(graph, samples):
	mu_s=np.empty((len(graph.nodes), 2))
	mu_st=np.empty((len(graph.nodes), len(graph.nodes), 4))
	n=len(samples)
	for sample in samples:
	