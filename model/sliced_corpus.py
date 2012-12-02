import nltk
from nltk.collocations import *


class sliced_corpus:

	def __init__(self, ids, timesteps, adjacency, docs):
		self.ids = ids
		self.timesteps = timesteps
		self.adjacency = adjacency
		self.docs = docs
		self.contagion = False


	def get_adjacency_graph(self):
		return self.adjacency

	def get_contagion_graph(self):
		if self.contagion = False:
			self.get_all_infections()
		return self.contagion

	def get_all_infections(self):
		infections = []
		lower_length = 2
		lower_frequency = 6
		trigrams = self.get_good_ngrams(corpus, 3)

		trees = []
		for trigram in trigrams:
			tree = self.get_infection_tree(trigram)
			if is_infection(tree):
				trees.append(tree)
		for tree in trees:
			self.fill_in_graph(tree)
		return infections

	def get_all_infections_netinf(self):
		infections = self.get_all_infections()
		return[self.clean(infection) for infection in infections]

	def clean(self, infection):
		seen = []
		for item in infection:
			if item[2] not in seen:
				seen.append(item[2])
			else:
				infection.remove(item)
		return infection

	def get_infection_tree(self, word):
		tree = []
		for timestep in timesteps.keys():
			for site in ids.keys():
				if word in docs.get(id, timestep):
					tree.append(timesteps[timestep], ids[site])
		return tree

	def is_infection(self, tree):
		counts = [0 for num in range(10)]
		interval = len(self.timesteps)/10
		for item in tree:
			counts[item(0)/interval] += 1
		if max(counts) > 2 * min(counts):
			return True
		else:
			return False