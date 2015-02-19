import os
import sys

if len(sys.argv) > 1:
	if sys.argv[1] == "restart":
		os.system("python init_scrape.py 1")
		os.system("python get_artist_corpus.py 1")
		os.system("python get_random_articles.py 1")
		os.system("python get_random_corpus.py 1 ")
		os.system("python language_test.py 1")

os.system("python get_pop.py 1")