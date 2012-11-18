import numpy as np
from ReddiWrap import ReddiWrap
from time import sleep

# I guess the thing to do is to index the top several thousand subs (readers geq 10?)
# then for each sub, gather the name of all commentors in the last say month.
# have a big n by n array of the top however many subs (5k)
# and a hash of various users (has been indexed)
class Graph():

	def __init__(self):
		self.reddit = ReddiWrap(user_agent='MadeThisUpQuick is trying to map users')
		self.min_subreddit_size = 1000
		self.pages_per_subreddit = 3
		self.indexed_users = set()
		self.subs = dict()
		self.get_big_subs()
		print 'Found {0} subreddits with at least {1} subscribers'.format(len(self.subs), self.min_subreddit_size)
		self.graph = np.zeros((len(self.subs), len(self.subs)))
		while True:
			print 'Scraping started.'
			new_users = set()
			# get all the users in each subreddit that we are not yet tracking
			print '\tFinding new subreddit users...'
			for sub in self.subs.keys():
				print 'Subreddit: {0}'.format(sub)
				new_users &= self.get_new_users(sub)
			# increment the edge weights based on the new users' subscriptions
			print '\tUpdating matrix for new users...'
			for i, user in enumerate(new_users):
				user_subs = self.get_subs(user)
				self.fill_in(user_subs)
				self.indexed_users.add(user)
			# Save every 100 iterations
			print '\tSaving adjacency matrix...'
			np.save("adjacencies.npy", self.graph)
			print 'Finished scraping iteration. Starting over...'
	
	def get_big_subs(self):
		subs = self.reddit.get('/reddits')
		while True:
			big_sub_found = False
			for sub in subs:
				print 'Candidate sub {0} with {1} subscribers'.format(sub.display_name, sub.subscribers)
				if sub.subscribers >= self.min_subreddit_size:
					self.subs[sub.display_name] = len(self.subs)
					big_sub_found = True
			if not big_sub_found:
				break
			sleep(2)
			subs = self.reddit.get_next()

	def get_new_users(self, sub):
		users = set()
		sleep(2)
		posts = self.reddit.get('/r/{0}'.format(sub))
		for i in range(self.pages_per_subreddit):
			if self.reddit.has_next():
				sleep(2)
				posts += self.reddit.get_next()
		for post in posts:
			print '\t\tPost: {0}'.format(post.name)
			users &= self.get_participants(post)
		users = [user for user in users if user not in self.indexed_users]
		return frozenset(users)

	def get_participants(self, post):
		sleep(2)
		self.reddit.get(post.url)
		participants = [comment.author for comment in post.comments]
		participants.append(post.author)
		return frozenset(participants)

	def get_subs(self, user):
		user_subs = [comment.subreddit for comment in self.reddit.get_user_comments(user, 'new')]
		user_subs &= [post.subreddit for post in self.reddit.get_user_posts(user, 'new')]
		return frozenset(user_subs)

	def fill_in(self, user_subs):
		for sub in user_subs:
			for sub2 in user_subs:
				if self.subs.has_key(sub) and self.subs.has_key(sub2):
					self.graph[self.subs[sub], self.subs[sub2]] += 1

def main():
	g = Graph()

if __name__ == "__main__":
    main()