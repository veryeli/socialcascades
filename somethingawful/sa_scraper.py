import urllib2
import sys
sys.path.append("/usr/local/share/python")
sys.path.append("/usr/local/lib/python2.7/site-packages")
from bs4 import BeautifulSoup, SoupStrainer
import time
import re, string


def get_name(base_url, link_url):
	links = []
	soup = get_soup(base_url)
	for a in soup.findAll('title'):
		try:
			print str(a).split('<title>')[1].split('-')[0].strip()
			return str(a).split('<title>')[1].split('-')[0].strip()
		except:
			return ""


def get_links_matching(base_url, link_url):
	print "Getting links..."
	links = []
	soup = get_soup(base_url)
	for a in soup.findAll('a'):
		if link_url in a['href']:
			if 'forums' in a["href"]:
				links.append(a["href"])
			else:
				links.append(base_url + a['href'])
	return links

def get_thread_pages(base_url, link_url):
	links = []
	soup = get_soup(base_url)
	for a in soup.findAll('a'):
		if link_url in a['href']:
			links.append('http://forums.somethingawful.com/' + a['href'])
	return links

def get_all_users(url):
	soup = get_soup(url)
	body = soup.body
	a = body.find_all('td')

	for item in a:
		for line in str(a).split('\n'):
			if 'title=' in line:
				user = line.split('>')[1].split('<')[0].strip()
				if len(user.split(' ')) < 2:
					users.append(user)

	users = set(users)
	return users

def get_all_pages(url):
	soup = get_soup(url)
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


def get_soup(url):
	try:
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)
	except:
		print "Unparseable:" + url
		return []
	return soup


def get_all_comments(url):
	comments = []
	soup = get_soup(url)
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
	return comments
