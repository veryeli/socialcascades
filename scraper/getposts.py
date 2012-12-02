import time
import datetime
from ReddiWrap import ReddiWrap
import numpy as np


reddit = ReddiWrap() # Create new instance of ReddiWrap
login_result = reddit.login('ahoytestaccount', 'isminus1')
try:
	postinfos = [item in np.load('text.npy')]
	indexed = [item in np.load('indexed.npy')]
except:
	indexed = []
	postinfos = []

while True:
	loaded = False
	while not loaded:
		#try:
			postholder = np.load('records.npz')
			posts = postholder['posts']
			loaded = True
		#except:
			time.sleep(3)
			print "failed"
	first_time = posts[0].created
	for post in [posts[-1 -num] for num in range(len(posts))]:
		print (first_time - post.created) / (60 * 60 * 24)
		if first_time - post.created > 60 * 60 * 24:
			if post.id not in indexed:
				time.sleep(2)
				print 'ok'
				indexed.append(post.id)
				reddit.fetch_comments(post)
				postinfos.append(post)
				np.save('text.npy',np.array(postinfos))
				np.save('indexed.npy', np.array(indexed))
	
	del postholder.f
	postholder.close()