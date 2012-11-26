import numpy as np
from ReddiWrap import ReddiWrap
from time import sleep
import csv

# Index the top several thousand subs (readers >= 1000)
# then for each sub, gather the name of all commentors in the last 5 pages of links.
# Have a big n by n array of the top however many subs (5k)
# and a hash of various users (has been indexed)
class Graph():

	def __init__(self):
		self.reddit = ReddiWrap(user_agent='made_this_up_quick')
		self.min_subreddit_size = 1000
		self.pages_per_subreddit = 5
		self.load_users()
		self.subs = dict()
		self.get_big_subs()
		print 'Found {0} subreddits with at least {1} subscribers'.format(len(self.subs), self.min_subreddit_size)
		self.graph = np.zeros((len(self.subs), len(self.subs)))
		self.user_indexes = []
		while True:
			print 'Scraping started.'
			new_users = self.load_new_users()
			# get all the users in each subreddit that we are not yet tracking
			print '\tFinding new subreddit users...'
			for sub in self.subs.keys():
				print '\t\tSubreddit: {0}'.encode('utf-8').format(sub.encode('utf-8'))
				new_users |= self.get_new_users(sub)
			# increment the edge weights based on the new users' subscriptions
			print '\tUpdating matrix for new users...'
			for i, user in enumerate(new_users):
				print '{0}: {1}'.encode('utf-8').format(i, user.encode('utf-8'))
				user_subs = self.get_subs(user)
				self.fill_in(user_subs)
				self.indexed_users.add(user)
			# Save every 100 iterations
			print '\tSaving adjacency matrix...'
			np.save("adjacencies.npy", self.graph)
			#self.save_matrix()
			print 'Finished scraping iteration. Starting over...'
	
	def get_big_subs(self):
		# if we already have the list, just load it from file
		if file.exists('subreddits.csv')
			load_subs()
			return
		# otherwise, build the list
		subs = self.reddit_get('/reddits')
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
		# save the list to file so we do not have to load it multiple times
		save_subs()

	def get_new_users(self, sub):
		users = set()
		posts = self.reddit_get('/r/{0}'.format(sub))
		for i in range(self.pages_per_subreddit):
			if self.reddit.has_next():
				sleep(2)
				posts += self.reddit.get_next()
		for post in posts:
			print '\t\t\t{0}'.encode('utf-8').format(post.permalink.encode('utf-8'))
			users |= self.get_participants(post)
		users = [user for user in users if user not in self.indexed_users]
		return frozenset(users)

	def get_participants(self, post):
		posts = self.reddit_get(post.permalink)
		post = posts[0]
		participants = [comment.author for comment in post.comments if comment.author != "[deleted]"]
		if(post.author != "[deleted]"):
			participants.append(post.author)
		result = frozenset(participants)
		return result

	def get_subs(self, user):
		user_subs = [comment.subreddit for comment in self.reddit.get_user_comments(user, 'new')]
		user_subs += [post.subreddit for post in self.reddit.get_user_posts(user, 'new')]
		return frozenset(user_subs)

	def fill_in(self, user_subs):
		for sub in user_subs:
			for sub2 in user_subs:
				if self.subs.has_key(sub) and self.subs.has_key(sub2):
					self.graph[self.subs[sub], self.subs[sub2]] += 1

	def load_subs(self):
		reader = open('subreddits.csv', 'r')
		for line in reader.readlines():
			tokens = line.split(',')
			self.subs[tokens[0]] = int(tokens[1])

	def load_users(self):
		self.indexed_users = set()
		if not file.exists('indexed_users.csv'):
			return
		reader = open('indexed_users.csv', 'r')
		for line in reader.readlines():
			tokens = line.split(',')
			self.indexed_users.add(tokens[0])

	def load_new_users(self):
		new_users = set()
		if not file.exists('new_users.csv', 'r'):
			return new_users
		reader = open('new_users.csv', 'r'):
		
		return new_users
	def save_subs(self):
		writer = csv.writer(open('subreddits.csv', 'wb'))
		for key, value in self.subs.items():
			writer.writerow([key, value])

	def save_matrix(self):
		writer = csv.writer(open('adjacencies.csv', 'wb'))
		for i in range(0,len(self.subs)):
			writer.writerow(self.graph[i,:])

	def reddit_get(self, url):
		sleep(2)
		result = self.reddit.get(url)
		wait_time = 3
		while result is None:
			print "failed. waiting {0} seconds and trying again...".format(wait_time)
			sleep(wait_time)
			result = self.reddit.get(url)
			wait_time = wait_time * 2
		return result

def main():
	g = Graph()

if __name__ == "__main__":
    main()

