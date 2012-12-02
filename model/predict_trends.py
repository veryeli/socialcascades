from gensim import corpora, models, similarities

f = pickle.load("alltext", "rb")

corpora = f['corpora']
corpus_list = f['corpus_list']

lsis = {}
similarities = []
for corpus in corpora.keys():
	# Initialize a transformation (Latent Semantic Indexing with 200 latent dimensions).
	lsis[corpus] = models.LsiModel(corpus, num_topics=200)
	for comparison_corpus in corpora.keys()

		# Convert another corpus to the latent space and index it.
		index = similarities.MatrixSimilarity(lsi[comparison_corpus])

		# determine similarity of a query document against each document in the index
		similarities[corpus_list[corpus]][corpus_list[comparison_corpus]] = index[query]

pring f["adjacency_graph"]

print similarities

sliced_corpora = f['sliced_corpora']

for time in range(f['num_timesteps']):
	trending_graph = get_trends(sliced_corpora, time)
	trending_vector = get_world_trends(sliced_corpora, time)





def get_trends(sliced_corpora, time):
	trends = {}
	for corpus in sliced corpora:
		train = ""
		for i in range(time-1):
			train+= sliced_corpora[corpus, i]
		lsi = models.LsiModel(train, num_topics=200)
		# find differences in sliced_corpora[corpus, time]