import time
import datetime
from ReddiWrap import ReddiWrap
import numpy as np

reddit = ReddiWrap() # Create new instance of ReddiWrap
login_result = reddit.login('brainsareneat', 'isminus1')

if login_result != 0: # Anything other than '0' means an error occurred
  print 'unable to log in.'
  exit(1)

olddict = {}
newdict = {}

clock = datetime.datetime

a = clock.now()
f = open("%s_%s_%srecord.csv" %(a.month, a.day, a.hour), "a")
f.write("id, author, subreddit, title, created, link, url")


b = clock.now()

while b - a < datetime.timedelta(hours=6):
	print b - a
	time.sleep(1)
	new = reddit.get('/r/all/new')
	seen = False
	for post in new:
		entry = {"subreddit":post.subreddit.encode('ascii', 'ignore'), "link":post.permalink.encode('ascii', 'ignore'), "title":post.title.encode('ascii', 'ignore'),\
			"created":post.created, "id":post.id, "url":post.url.encode('ascii', 'ignore'), "author":post.author.encode('ascii', 'ignore')}
		if olddict.has_key(post.id):
			seen = True
		elif not newdict.has_key(post.id):
			newdict[post.id]=entry
	if not seen:
		for item in olddict.values():
			f.write("%s,%s,%s,%s,%s,%s,%s\n" %(item["id"], item["author"], item["subreddit"], item["title"],\
				item["created"], item["link"], item["url"]))
		olddict=newdict
		newdict={}
	b = clock.now()

#construct user/subreddit relationships
#a user is relatedto a subreddit if they submit to or comment on it 




