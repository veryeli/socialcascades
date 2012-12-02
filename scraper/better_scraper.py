import time
import datetime
from ReddiWrap import ReddiWrap
import numpy as np

reddit = ReddiWrap() # Create new instance of ReddiWrap
login_result = reddit.login('brainsareneat', 'isminus1')

all_posts = []
new = reddit.get('/r/all/new')

while True:
	time.sleep(1.5)
	for post in new:
		all_posts.append(post)
	posts= np.array(all_posts)
	np.savez('records.npz', posts = posts)	
	new = reddit.get_next()
	print 'ok...'