import init_scrape
import get_random_corpus
import get_artist_corpus
import get_random_articles
import requests
from cleaners import clean_for_words
from artist import Artist

START = '<extract xml:space="preserve">'
artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
randoms = open(get_random_articles.RANDOM_ARTICLES,'r').read().split("\n")
a_file = "../data/readable/a_words.txt"
r_file = "../data/readable/r_words.txt"

SIZE = 5000

def identifiers(size):
	r_hash = {line.split(",")[0]:float(line.split(",")[1]) for line in open(get_random_corpus.RANDOM_CORPUS, 'r').read().split("\n")}
	a_hash = {line.split(",")[0]:float(line.split(",")[1]) for line in open(get_artist_corpus.ARTIST_CORPUS,'r').read().split("\n")}
	a_common = sorted(a_hash, key=a_hash.get, reverse=True)[1:size] 
	r_common = sorted(r_hash, key=r_hash.get, reverse=True)[1:size]
	diff = [[x for x in a_common if x not in r_common],[x for x in r_common if x not in a_common]]
	
	open(a_file,'w').write(",".join(diff[0]))
	open(r_file,'w').write(",".join(diff[1]))
	return diff

def which(tokens):
	#artist = true, random = false
	a_common = identifiers(SIZE)[0]
	r_common = identifiers(SIZE)[1]
	a_words = [a for a in tokens if a in a_common]
	r_words = [r for r in tokens if r in r_common]
	return len(a_words) > len(r_words)

def alt():
	for artist in artists:
		data = clean_for_words(artist.get_data())
		print str(which(data)) + " " + artist.name + " ARTIST"
	for random in randoms:
		HEADER = init_scrape.HEADER
		FOOTER = "action=query&prop=extracts&titles=%s&redirects=true&format=xml"%(random.replace("&","%26"))
		data = clean_for_words(requests.get(HEADER + FOOTER).text.encode('utf8'))
		print str(which(data)) + " " + random + " RANDOM ARTICLE"
	

def main():
	alt()
if __name__ == "__main__":
	main()
