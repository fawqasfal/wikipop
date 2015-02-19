import init_scrape
import requests
from artist import Artist
import os
from collections import Counter
from cleaners import fix_punct, clean_for_words, list_in
from artist import Artist 
import sys
import get_random_articles


START = '<extract xml:space="preserve">'
RANDOM_WORDS = "../data/readable/random_words.txt"
RANDOM_CORPUS = "../data/readable/random_corpus.txt"

def get_random_words(article_names):
	print "Getting words of the articles from the random article names."
	answer = ""
	for name in article_names:
		file_name = "../data/random/%s.txt"%(name.replace("/","\\"))
		if os.path.isfile(file_name):
			answer += open(file_name,'r').read()
			continue
		FOOTER = "action=query&prop=extracts&titles=%s&redirects=true&format=xml"%(name.replace("&","%26"))
		HEADER = init_scrape.HEADER
		text = fix_punct(requests.get(HEADER + FOOTER).text.encode('utf8'))
		if START in text:
			print name
			article = text[text.index(START) + len(START):]
			append = clean_for_words(article)
			open(file_name,'w').write("\n".join(append))
			answer += "\n".join(append)
	return answer

def write(artists):
	r_words = get_random_words(open(get_random_articles.RANDOM_ARTICLES, 'r').read().split("\n"))
	open(RANDOM_WORDS,'w').write(r_words)
	return r_words

def main():
	print "Getting corpus of words from random articles."
	if len(sys.argv) > 1 and sys.argv[1] == 'new':
		print "Getting words."
		artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
		r_words = write(artists).split("\n")
	else:
		r_words = open(RANDOM_WORDS,'r').read().split("\n")
	print str(len(r_words)) + " Random words."
	print "Making frequency table."
	random_dict = Counter(r_words)
	r_write = ["%s,%d"%(key, random_dict[key]) for key in random_dict.keys()][1:]
	open(RANDOM_CORPUS,'w').write("\n".join(r_write))

if __name__ == "__main__":
	main()
