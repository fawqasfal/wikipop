import init_scrape
import get_random_articles
import get_random_corpus
import get_artist_corpus
import operator
import requests
import os
import cleaners

from cleaners import clean_for_words, fix_punct
from artist import Artist
START = '<extract xml:space="preserve">'
artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
randoms = open(get_random_articles.RANDOM_ARTICLES,'r').read().split("\n")
rhash = {line.split(",")[0]:float(line.split(",")[1]) for line in open(get_random_corpus.RANDOM_CORPUS, 'r').read().split("\n")}
ahash = {line.split(",")[0]:float(line.split(",")[1]) for line in open(get_artist_corpus.ARTIST_CORPUS,'r').read().split("\n")}

def third_hash(a_hash, r_hash, len_a, len_r):
	#len_artists is number of artist articles, NOT number of artist words.
	#len_random is number of random articles, NOT number of random words.
	words = a_hash.keys() + r_hash.keys()
	r_probs = {}
	for i in xrange(len(words)):
		if words[i] not in a_hash:
			good = 0
		else:
			good = a_hash[words[i]]
		if words[i] not in r_hash:
			bad = 0
		else:
			bad = r_hash[words[i]]
		if bad + good >= 5:
			prob_word_r = 2.75  * min(0.99, max(.01, float(bad) / float(len_r)))
			prob_word_a = min(0.99, max(.01, float(good) / float(len_a)))
			prop_rand = float(len_r / (len_a + len_r))
			prop_art = 1 - prop_rand
			prob_rand = (prob_word_r) / (prob_word_a + prob_word_r)
			r_probs[words[i]] = prob_rand
	return r_probs

def prob_rand(data):
	hash_words = third_hash(ahash, rhash, len(artists), len(randoms))
	probs = [hash_words[item] for item in data if item in hash_words]
	probs = sorted(probs, key=lambda x: abs(x - 0.5), reverse = True)
	probs = probs[:15]
	mul_prob = reduce(operator.mul, probs)
	opp_probs = [1 - prob for prob in probs]
	mul_opp = reduce(operator.mul, opp_probs)
	if mul_prob == 0.0 and mul_opp == 0.0:
		return 0.0
	final_prob = mul_prob / (mul_prob + mul_opp)
	return final_prob


def check_artists():
	new_artists = []
	"""for artist in artists:
		bad = ["Minneapolis, Minnesota", "New York City, New York", "Denver, Colorado", "Portland, Oregon", "Seattle, Washington",
		"Aberdeen, Washington", "Austin, Texas", "Salt Lake City, Utah", "Orlando, Florida"]
		if artist.name in bad:
			data = clean_for_words(artist.get_data())
			print str(naive_test.which(data)) + " " + artist.name 
			print prob_rand(data)"""

	for artist in artists:
		if os.path.isfile("../data/prob/" + artist.name.replace("/","\\")): 
			prob = float(open("../data/prob/" + artist.name.replace("/","\\"), 'r').read())
		else: 
			data = clean_for_words(artist.get_data())
			prob = prob_rand(data)
			open("../data/prob/" + artist.name.replace("/","\\"), 'w').write(str(prob))
		if prob > 0.20 and "musician)" not in artist.name:
			print "ERROR!"
			print artist.name + ", a supposed artist article, has a probability of " + str(prob) + " of being a random article."
			print "It has been eliminated from consideration as an artist."
		else:
			print artist.name + ", a supposed artist article, has a probability of " + str(prob) + " of being a random article."
			new_artists.append(artist.name)

	open(init_scrape.CLEAN,'w').write("\n".join(new_artists))

def main():
	check_artists()

if __name__ == "__main__":
	main()


