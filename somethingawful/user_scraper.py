import sa_scraper
import numpy as np

def main():
	base_url = "http://forums.somethingawful.com/"
	forae = set(get_links_matching(base_url, 'forumdisplay.php?forumid'))
	entry_id = 0
	recorded = []
	print len(forae)
	for item in forae:
		print '"' + item.split('=')[-1] + '"',
	for forum in forae:
		if forum in recorded:
			break
		else:
			recorded.append(forum)
		print "recording forum" + forum
		f = open(forum.split('=')[1], 'w')
		print 'forum:' + forum.split('=')[1]
		for forum_page in get_all_pages(forum):
			print "On a new forum PAGE...."
			thread_urls = get_thread_pages(forum_page, 'showthread.php?threadid')
			for thread_page in thread_urls:
				print "On a new thread page...."
				comments = get_all_users(thread_page)
				for comment in comments:
					if len(comment) > 0:
						f.write('Commenter: %s' %comment)
						print comment
						entry_id += 1


main()