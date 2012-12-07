from sa_scraper import *

def main():
	base_url = "http://forums.somethingawful.com/"

	forae = set(get_links_matching(base_url, 'forumdisplay.php?forumid'))
	entry_id = 0
	recorded = []
	print len(forae)
	for item in forae:
		print '"' + item.split('=')[-1] + '"',
	for forum in forae:
		if forum.split('=')[-1] == '1':
			break
		if forum in recorded:
			break
		else:
			recorded.append(forum)
		print "recording forum" + forum
		f = open(forum.split('=')[1], 'w')
		f.write('<?xml version="1.0" encoding="utf-8"?>\n<posts>\n')
		for forum_page in get_all_pages(forum):
			print "On a new forum PAGE...."

			thread_urls = get_thread_pages(forum_page, 'showthread.php?threadid')
			for thread_page in thread_urls:
				print "On a new thread page...."
				comments = get_all_comments(thread_page)
				for comment in comments:
					if len(comment[1]) > 0:
						f.write('<Row Id="%s" %s %s />\n' %(entry_id, comment[1], comment[0]))
						entry_id += 1
		f.write("</posts>")

main()