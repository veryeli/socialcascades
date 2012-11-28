import numpy as np
from ReddiWrap import ReddiWrap
import time
import pickle
import sys
# I guess the thing to do is to index the top several thousand subs (readers geq 10?)
# then for each sub, gather the name of all commentors in the last say month.
# have a big n by n array of the top however many subs (5k)
# and a hash of various users (has been indexed)
def main():

	reddit = ReddiWrap(user_agent='made_this_up_quick')
	reddit.login('brainsareneat', 'isminus1')
	outfile = "graph.pkl"
	g = Graph(reddit, outfile)
	while True:
		g.update()

class Graph():
	def __init__(self, reddit, outfile):
		self.size_lim = 5000
		self.reddit = reddit
		self.outfile = outfile
		self.load_info()
		self.save()
		self.i = 0

	def update(self):
		for sub in self.subs.keys():
			self.users |= self.get_new_users(sub)
			self.update_graph()
		self.save()

	def update_graph(self):
		for user in (self.users - self.indexed_users):
			print user
			self.fill_in(self.get_subs(user))
			self.indexed_users |= frozenset([user])
			time.sleep(1.75)
			self.i = self.i + 1
			if self.i % 100 == 0:
				self.save()

	def load_info(self):
		try:
			data = pickle.load(open(self.outfile, 'rb'))
			self.subs = data['subs']
			self.users = data['users']
			self.indexed_users = data['indexed_users']
			self.graph = data['graph']
		except:
			self.subs = self.get_big_subs(self.size_lim)
			self.users = frozenset()
			self.indexed_users = frozenset()
			self.graph=np.zeros((len(self.subs),len(self.subs)))


	def get_new_users(self, sub):
		users = frozenset()
		posts = self.reddit_get('reddit.com{0}'.format(sub))
		for post in posts:
			print '\t\t\t{0}'.encode('utf-8').format(post.permalink.encode('utf-8'))
			users |= self.get_participants(post)
		users = [user for user in users if user not in self.indexed_users]
		self.save()
		return frozenset(users)

	def get_participants(self, post):
		posts = self.reddit_get(post.permalink)
		if len(posts) < 1:
			return frozenset([])
		post = posts[0]
		participants = [comment.author for comment in post.comments if comment.author != "[deleted]"]
		if(post.author != "[deleted]"):
			participants.append(post.author)
		result = frozenset(participants)
		return result


	def get_big_subs(self, size):
		subs = self.reddit.get('/reddits')
		i = 0
		big_subs = {}
		while True:
			for sub in subs: 
				print 'Candidate sub {0} with {1} subscribers'.format(sub.display_name, sub.subscribers)
				big_sub_found = False
				if sub.subscribers >= size:
					big_subs[sub.url]=i
					i += 1
					big_sub_found = True
			if not big_sub_found:
				break
			time.sleep(1.75)
			subs = self.reddit.get_next()
		return big_subs


	def get_subs(self, user):
		try:
			user_subs = [comment.subreddit for comment in self.reddit.get_user_comments(user, 'new')]
		except:
			print "no comments"
			user_subs = []
		time.sleep(1.5)
		try:
			user_subs += [post.subreddit for post in self.reddit.get_user_posts(user, 'new')]
		except:
			print "No submissions"
		if len(user_subs) > 0:
			user_subs = ['/r/' + sub + '/' for sub in user_subs]
		print frozenset(user_subs)
		self.save()
		return frozenset(user_subs)

	def fill_in(self, user_subs):
		for sub in user_subs:
			for sub2 in user_subs:
				if self.subs.has_key(sub) and self.subs.has_key(sub2):
					self.graph[self.subs[sub], self.subs[sub2]]+= 1

	def save(self):
		print "saving..............."
		obj = {"subs": self.subs, "users": self.users, "indexed_users": self.indexed_users, "graph": self.graph}
		pickle.dump(obj, open(self.outfile, 'wb'))

	def reddit_get(self, url):
		result = self.reddit.get(url)
		wait_time = 3
		if result is None:
			print "failed. waiting {0} seconds and trying again...".format(wait_time)
			time.sleep(wait_time)
			result = self.reddit.get(url)
		if result is None:
			print "failed" + url
			result = []		
		return result

main()