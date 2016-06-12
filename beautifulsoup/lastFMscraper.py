from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep

BASE_URL = "http://www.chicagoreader.com"
BASE_URL = "http://www.similar-artist.com/similarto/artistCatalog/ALL/"
BASE_URL = "http://www.last.fm/music/"

def get_category_links(section_url):
	soup = make_soup(section_url)
#	boccat = soup.find("div","discounted-item rnb music-playlist button-icon")
#	category_links = [h1.a["href"] for h1 in boccat.findAll("h1")]
	simArtists = soup.findAll("a","link-block-target")
	artistList = [a.text for a in simArtists]
	
	print artistList
	#return category_links

def get_category_winner(category_url):
	soup = make_soup(category_url)
	category = soup.find("h1", "headline").string
	winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
	runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
	return {"category": category,
		"category_url": category_url,
		"winner": winner,
		"runners_up": runners_up}

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, "lxml")

if __name__ == '__main__':

	artist = "The+Decemberists"

	categories = get_category_links(BASE_URL + artist + "/+similar")
	#print categories
'''	
	data = []
	for category in categories:
		winner = get_category_winner(category)
		data.append(winner)
		sleep(1)

	print data
'''
