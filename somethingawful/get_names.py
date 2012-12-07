from sa_scraper import *
import numpy as np

def main():
	base_url = "http://forums.somethingawful.com/"
	forae = set(get_links_matching(base_url, 'forumdisplay.php?forumid'))
	entry_id = 0
	names = {}
	recorded = []
	print len(forae)
	for forum in forae:
		if forum in recorded:
			break
		else:
			recorded.append(forum)
		f = open(forum.split('=')[1], 'w')
		for forum_page in get_all_pages(forum):
			name = get_name(forum_page, 'showthread.php?threadid')
			names[forum.split('=')[1]] = name
	print names
	np.savez("names.npz", names=names)

main()