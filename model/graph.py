class Graph:
	def __init__(self, sites):
		self.dict = {}
		self.nodes = {}
		self.edges = {}
		self.num_nodes = len(sites)
		self.init_dict(sites)
		self.init_nodes()
		self.init_edges()
	

	def init_dict(self, sites):
		i = 0
		for site in sites:
			self.dict[i]=site
			i += 1

	def init_nodes(self):
		for i in range(len(self.dict.keys())):
			self.nodes[str(i)] = 0
			self.nodes[str(i)+'*']=0

	def init_edges(self):
		for i in range(len(self.dict.keys())):
			for j in range(len(self.dict.keys())):
				self.edges[(str(i), str(j)+'*')] = 0
		for i in range(len(self.dict.keys())):
			for j in range(len(self.dict.keys())):
				if i != j:	
					self.edges[(str(i)+'*', str(j)+'*')] = 0

	def learn_parameters(self, samples):
		# Assume examples is an assignment to nodes at time t and t+1
		# examples should be (dict1, dict2) where dict1 =(sitename: 1 or 0,....)
		mu_s=np.empty((len(graph.nodes) * 2, 2))
		mu_st=np.empty((len(graph.nodes), len(graph.nodes), 4))
		n=len(samples)
		for sample in samples:
			for node in self.nodes.keys():
				node_num = int(node[:-1] if '*' in node else nodes)
				node_id = self.dict(node_num)
				node_val = sample[0][node_id]
				if '*' not in node:
					mu_s[node_num, node_val] += 1
				else:
					mu_s[self.num_nodes + node_num, node_val] += 1


	def get_sample_val(sample, node):

	def get_sample_edge(sample, node1, node2):


	def get_node_id(node):
		node_num = int(node[:-1] if '*' in node else nodes)
		node_id = self.dict(node_num)
