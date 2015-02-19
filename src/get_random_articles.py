import init_scrape
import requests
from cleaners import list_in, fix_punct
from artist import Artist
RANDOM_ARTICLES = "../data/readable/random_articles.txt"
MAX = 10
def get_random_article_names(limit):
	#gets names of the random articles we're going to scrape. 
	FOOTER = "action=query&list=random&rnlimit=%d&format=xml"%(limit)
	HEADER = init_scrape.HEADER
	article = requests.get(HEADER + FOOTER).text.encode('utf8') #gives you "limit" amt of names of random articles
	names = article.split("title=")
	cleaned = [name[:name.index(" />")] for name in names[1:]]
	return cleaned


def good_article_names(limit, artists):
	#scrapes random articles
	print "Getting random article names."
	answer = []
	artist_names = [artist.name for artist in artists]
	bad = ["talk:", "User:", "Template:", "Talk:", "Portal:", "File:", "Wikipedia:", "Category:", "Book:", "MediaWiki:", "Draft:"]
	#these meta articles that aren't about real-world stuff and are not formatted like most articles are are not allowed
	while len(answer) < limit:
		attempts = get_random_article_names(MAX)
		for attempt in attempts:
			fixed_attempt = fix_punct(attempt)
			if not list_in(fixed_attempt, bad) and fixed_attempt not in artist_names: #random articles are not allowed to be artists
				answer.append(fixed_attempt.strip('"')) 
				print fixed_attempt
	print str(len(answer)) + " Random articles."
	open(RANDOM_ARTICLES,'w').write("\n".join(answer))
	return answer

def main():
	artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
	articles = good_article_names(len(artists), artists)
	return articles

if __name__ == "__main__":
	main()
