import pretty_graph
import sys
import numpy as np


def main(args):

	m = np.random.rand(40,40)
	pretty_graph.graph_matrix(m)

	sys.exit()
	dataset_file = args[1]
	complete_graph_outfile = args[2]
	netinf_outfile = args[2]
	
	#load up corpus
	c = sliced_corpus(args[1])

	# generate adjacency graphs
	pretty_graph.graph_complete_matrix("Adjacency",c.get_adjacency_graph())
	# generate contagion graphs
	pretty_graph.graph_complete_matrix("Contagion",c.get_contagion_graph())	
	
	# generate netinf graph
	c.write_data_for_netinf(netinf_outfile)		

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




main(sys.argv)