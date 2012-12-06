import urllib
from bs4 import BeautifulSoup

base_url = "forums.somethingawful.com"

forae = get_links_matching(base_url+'forum_display.php?forumid=')

for forum in forae:
