import os
import sys

if len(sys.argv) > 1:
	if sys.argv[1] == "restart":
		os.system("python init_scrape.py")
		os.system("python get_artist_corpus.py")
		os.system("python get_random_articles.py")
		os.system("python get_random_corpus.py new")
		os.system("python language_test.py")

os.system("python get_pop.py")