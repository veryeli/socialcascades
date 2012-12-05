import pretty_graph
import sys
import numpy as np
import graph
from transform import transform_to_netinf

def main(args):
	if args[1] == 'test':
		test(args[2], args[3], args[4])

	#site_file = args[1]
	data_file = 'data/synthetic_5.csv'

	g=graph.Graph(range(5))

	#training_file = args[2]
	#training_file = 'data/synthetic_5.csv'
	g.learn_parameters(data_file)
	print g.edges

	#complete_graph_outfile = args[2]



	#netinf_outfile = args[2]
	
#	# generate adjacency graphs
#	pretty_graph.graph_complete_matrix("Adjacency",c.get_adjacency_graph())

	np.savez(data_file + ".npz", theta_st=g.edges, theta_s=g.nodes)

	pretty_graph.graph_matrix(np.load(data_file + ".npz")["graph"][3])	
	
	# generate netinf graph
	transform_to_netinf(data_file)		

#-----------------------------------
		#predicting

		# whether a node will be infected in next timestep
		# generate our graph with 9/10ths of trees
		# for other 10% of tree:
			# look @ graph at time t
			# predict new contagions at time t+1, t+2...
				# with our complete graph
				# with netinf incomplete graph

		# simulate data
		# repeat prediction task on simulated data		


def test(params_file, data_file_prefix, num_sites):
	results = []
	for fold in range(6):
		print "Fold %d of 6" % (fold)
		train_file = 'train' + str(fold)
		test_file  =  'test' +str(fold) 
		g = graph.Graph(range(num_sites))
		print "Learning parameters..."
		g.learn_parameters(train_file)
		print "testing...."
		results.append(g.test(test_file))
		numpy.savez(data_file_prefix + "results.npz", results=results)
	print "all done testing!"
	print results


main(sys.argv)