import pretty_graph
import sys
import numpy as np
import graph
import pickle
from transform import transform_to_netinf

def main(args):
	
	#site_file = args[1]
	#data_file = 'data/synthetic_5.csv'

	#g=graph.Graph(range(5))

	#training_file = args[2]
	#training_file = 'data/synthetic_5.csv'
	#g.learn_parameters(data_file)
	#print g.edges
	#np.savez("graph.npz", graph=g.edges)
	#reddit = pickle.load(open('graph.pkl'))


	#name_map = pickle.load(open('stackexchange_site_ids.data'))
	# name_map = reddit['subs']
	# names = ["" for x in range(0,len(name_map.keys()))]
	# for name in name_map.keys():
	# 	names[name_map[name]] = name
	# pretty_graph.graph_adj_matrix(reddit["graph"], names)
	names = {0: 'YCS Goldmine', 1: 'DIY and Hobbies', 2: 'Helldump Success Stories', 3: "Batmans Shameful Secret", 4: 'The Cavern of COBOL', 5: 'Business Finance and Careers', 6: "Musician Lounge", 7: 'Goons With Chickencheese', 8: 'Post Your Favorite', 9: 'Serious Hardware and Software Crap', 10: 'The Finer Arts', 11: 'Automotive Insanity', 12: 'Comedy Goldmine', 13: 'ADTRW', 14: 'Comedy Gas Chamber', 15: 'The MMO HMO', 16: 'Main', 17: 'Rapidly Going Deaf', 18: 'Inspect Your Gadgets', 19: "Lets Play", 20: 'Games', 21: 'Debate and Discussion', 22: 'General Bullshit', 23: 'The TV IV', 24: 'The Film Dump', 25: 'Haus of Tech Support', 26: 'The Dorkroom', 27: 'You Look Like Shit', 28: 'Tourism and Travel', 29: "SA Front Page Discussion", 30: 'LF Goldmine', 31: 'EN Bullshit', 32: 'A Blizzard Subforum', 33: 'Cinema Discusso', 34: 'No Music Discussion', 35: 'Goons in Platoons', 36: 'YOSPOS', 37: 'Third Street Skyrims Elder Saints The Fifth', 38: 'The Firing Range', 39: 'The Ray Parlour', 40: 'Archives', 41: 'Traditional Games', 42: 'Ask and Tell', 43: 'Punchsport Pagoda', 44: 'The Football Funhouse', 45: 'The Book Barn', 46: 'FYAD Criterion Collection', 47: 'Cycle Asylum', 48: 'Discussion', 49: 'Creative Convention', 50: 'Pet Island', 51: 'Sports Argument Stadium', 52: 'The Fitness Log Cabin', 53: 'The Armchair Quarterback'}
	for i in names:
		names[i] = names[i].replace(' ', '_')
	a = np.load("data/something_awful_adj_matrix.npz")
	g=a['g']
	print g.shape
	print len(names)
	pretty_graph.graph_adj_matrix(g, names, 'something_awful.gv')
	
	# generate netinf graph
	#transform_to_netinf(data_file)		

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