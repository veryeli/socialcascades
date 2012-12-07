import urllib2
import sys
sys.path.append("/usr/local/share/python")
sys.path.append("/usr/local/lib/python2.7/site-packages")
from bs4 import BeautifulSoup, SoupStrainer
import time
import re, string

def main():
	base_url = "http://forums.somethingawful.com/"

	forae = set(get_links_matching(base_url, 'forumdisplay.php?forumid'))
	entry_id = 0
	recorded = []
	print len(forae)
	for item in forae:
		print '"' + item.split('=')[-1] + '"',
	sys.exit()
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


def get_links_matching(base_url, link_url):
	print "Getting links..."
	links = []
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
	except:
		print "Unparseable:" + url
		return []
	for a in soup.findAll('a'):
		if link_url in a['href']:
			if 'forums' in a["href"]:
				links.append(a["href"])
			else:
				links.append(base_url + a['href'])
	return links

def get_thread_pages(base_url, link_url):
	links = []
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
	except:
		print "Unparseable:" + url
		return []
	for a in soup.findAll('a'):
		if link_url in a['href']:
			links.append('http://forums.somethingawful.com/' + a['href'])
	return links

def get_all_comments(url):
	comments = []
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
	except:
		print "Unparseable:" + url
		return []
	body = soup.body
	a = body.find_all('td')
	i = 0
	while i <len(a) - 3:
		text = a[i+1].text.encode("utf8")
		try:
			text = text.split('BeginContentMarker')[1]
		except:
			pass
		try:
			text=text.split("EndContentMarker")[0]
		except:
			pass
		text=text.replace('\n', ' ')
		text=text.replace('google_ad_section_start', ' ')
		text=text.replace('google_ad_section_end', ' ')
		text = text.strip()
		comments.append(('Body="'+ text +'"', get_date(a[i+2])))
		i+= 4
	print len(comments)
	return comments

def get_all_pages(url):
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
	except:
		print "Unparseable:" + url
		return []
	for a in soup.find_all("div"):
		try:
			div_class =  a["class"]
			if 'bottom' in div_class:
				if not 'Pages' in str(a):
					return [url]
				else:
					num_pages = int(str(a).split('(')[1].split(')')[0])
		except:
			pass
	head = url + "&daysprune=15&perpage=40&posticon=0&sortorder=desc&sortfield=lastpost&pagenumber="
	return [head + str(i) for i in range(1,num_pages + 1)]

def get_date(postdate):
	'CreationDate="2010-09-13T19:16:26.763"'
	if '2012' not in str(postdate):
		return ""
	try:
		posttime =  str(postdate).split('\n')[3].strip()
		date = posttime.split('2012')[0].replace(' ','') + '2012'
		date = time.strptime(date, "%b%d,%Y")
		date = time.strftime("%Y-%m-%d", date)
		hourmin = posttime.split('2012')[1].strip()
		return 'CreationDate="%sT%s:00.000"' %(date, hourmin)
	except:
		print "Unparseable date"
		print "postdate"
		return ""

main()