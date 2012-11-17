# I guess the thing to do is to index the top several thousand subs (readers geq 10?)
# then for each sub, gather the name of all commentors in the last say month.
# have a big n by n array of the top however many subs (5k)
# and a hash of various users (has been indexed)
class Graph():

	def __init__(self, reddit)
	size_lim = 1000
	self.reddit = reddit()
	self.subs = set()
	self.users = set()
	self.indexed_users = set()

	self.graph=np.array(len(self.subs), len(self.subs))

	while True:
		self.subs = self.subs.union(self.get_big_subs(100))
		for sub in self.subs:
			self.users = self.users.join(self.get_new_users(sub))
		i = 0
		for user in self.users:
			user_subs = self.get_subs(user)
			self.fill_in(user_subs)
			i += 1
			if i % 100 == 0:
				save(graph)


	def get_new_users(self, sub):
		users = set()
		posts = reddit.get('/%s' %(sub))
		for post in posts:
			users = users.join(get_participants(post))
		while reddit.has_next():
			posts = reddit.get_next()
			users = users.join(get_participants(post))
		users = [user for user in users where user not in self.indexed_users]
		return set(users)

	def get_participants(self, post):
		participants = set()
		reddit.get(post)
		participants = post.author
		for comment in post.comments:
			participants = participants.join(comment.author)
		return participants


	def get_big_subs(self, size):
		subs = reddit.get('/reddits')
		i = 0
		while True:
			for sub in subs: 
				big_sub_found = False
				if sub.subscribers >= size:
					self.subs[sub.id] = i
					i += 1
					big_sub_found = True
			if not big_sub_found:
				break
			subs = reddit.get_next()


	def get_subs(self, user):
		user_subs = [comment.subreddit for comment in self.reddit.get_user_comments(user, 'new')]
		user_subs = user_subs.join([post.subreddit for post in self.reddit.get_user_posts(user, 'new')])
		return user_subs

	def fill_in(self, user_subs):
		for sub in user_subs:
			for sub2 in user_subs:
				if self.subs.has_key(sub) and self.subs.has_key(sub2):
					self.graph(self.subs[sub], self.subs[sub2]) += 1	