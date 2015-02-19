import init_scrape
import requests
from artist import Artist
import os
from collections import Counter
from cleaners import fix_punct, clean_for_words
from artist import Artist 

START = '<extract xml:space="preserve">'
ARTIST_CORPUS = "../data/readable/artist_corpus.txt"
ARTIST_WORDS = "../data/readable/artist_words.txt"
def get_words(artists):
	answer = ""
	for artist in artists:
		article = artist.get_data()
		if START in article:
			article = article[article.index(START) + len(START):]
			answer += "\n".join(clean_for_words(article))
	return answer

def write(artists):
	a_words = get_words(artists)
	open(ARTIST_WORDS,'w').write(a_words)
	print str(len(a_words)) + " Artist words."
	return a_words

def main():
	print "Getting corpus of artist words."
	artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
	a_words = write(artists).split("\n")
	print "Making frequency table."
	a_dict = Counter(a_words)
	a_write = ["%s,%d"%(key, a_dict[key]) for key in a_dict.keys()][1:]
	open(ARTIST_CORPUS,'w').write("\n".join(a_write))

if __name__ == '__main__':
	main()