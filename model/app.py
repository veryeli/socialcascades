import pretty_graph
import sys
import numpy as np
import graph
import pickle

def main(args):


	#site_file = args[1]
	#site_file = 'data/infections_daily.csv'

	#g=graph.Graph(range(60))

	#training_file = args[2]
	#training_file = 'data/infections_daily.csv'
	#g.learn_parameters(training_file)
	#print g.edges

	#complete_graph_outfile = args[2]



	#netinf_outfile = args[2]
	
#	# generate adjacency graphs
#	pretty_graph.graph_complete_matrix("Adjacency",c.get_adjacency_graph())

	#np.savez("graph.npz", graph=g.edges)
	reddit = pickle.load(open('graph.pkl'))

	#name_map = pickle.load(open('stackexchange_site_ids.data'))
	name_map = reddit['subs']
	names = ["" for x in range(0,len(name_map.keys()))]
	for name in name_map.keys():
		names[name_map[name]] = name
	pretty_graph.graph_adj_matrix(reddit["graph"], names)	
	
	# generate netinf graph
	#c.write_data_for_netinf(netinf_outfile)		

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