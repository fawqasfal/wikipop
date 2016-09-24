import requests 
import os 
from cleaners import fix_punct, clean_data, red
import operator
START = '<extract xml:space="preserve">'

"""def dict_index(name):
	if ord(name[0].upper()) not in xrange(ord('A'), ord('Z') + 1):
		return 'NONE'
	else:
		return name[0].upper()"""


class Artist(object):
	ARTISTS = open("../data/readable/final_clean_data.txt",'r').read().split("\n")
	HEADER = "https://en.wikipedia.org/w/api.php?" #header string for all API calls
	#DICT_FILE = "../data/readable/final_clean_dict.txt"
	LENGTH = len(open("../data/readable/final_clean_data.txt",'r').read().split("\n"))
	DAMP = 0.85
	ITER = 10

	def __init__(self, name):
		self.name = name
		self.network_file = "../data/networks/" + self.name.replace('/','\\') + '.txt'
		self.to_file_name = "../data/to_links/" + self.name.replace('/','\\') + '.txt'
		self.pop_file = "../data/popularity/" + self.name.replace("/","\\") + '.txt'
		self.FOOTER = "action=query&prop=extracts&titles=%s&redirects=true&format=xml"%(name.replace("&","%26")) 
		self.XML_FOOTER = "action=query&titles=%s&prop=revisions&rvprop=content&format=xmlfm"%(name.replace("&","%26"))
		self.xml_file = "../data/xml_artists/%s.txt"%(name.replace("/","\\"))
		#'&' is a special character for the URL, so for requesting articles with '&' in the title, replace it with %26
		self.article = Artist.HEADER + self.FOOTER #full article title
		self.file = "../data/artists/%s.txt"%(name.replace("/","\\")) 
		#will contain all the XML data for this artist's article. unix filenames cannot have '/'
		self.memo = "" #saved string of article data
		self.get_data()

	def get_data(self):
		if self.memo != "":
		#if self.memo exists, then all the data has already been collected, stored on the hard drive, and put in self.memo
			return self.memo 
		elif os.path.isfile(self.file): 
		#if the file exists, but self.memo doesn't, then the data is stored from a previous time we executed the script.
		#re-assign the memo variable
			self.memo = open(self.file,'r').read()
			return self.memo
		else:
		#this is the very first time we're executing the script on this artist.
			self.memo = fix_punct(requests.get(self.article).text.encode('utf8'))
			print "Got data : " + self.name 
			#often 1st timeget_data()s are run on a whole corpus of artists,
			#so it's important to record progress by printing after each request
			open(self.file, 'w').write(self.memo)
			return self.memo

	def get_xml_data(self):
		if os.path.isfile(self.xml_file):
			return open(self.xml_file,'r').read()
		else:
			data = requests.get(Artist.HEADER + self.XML_FOOTER).text.encode('utf8')
			open(self.xml_file,'w').write(data)
			return data

	def set_links(self):
		x_data = self.get_xml_data()
		print "Setting links for " + self.name
		links = clean_data(x_data)
		if os.path.isfile(self.to_file_name):
			print "Already set links for this artist."
			return
		elif red(self) or START not in self.get_data():
			print "Faulty artist." 
			return
		a_links = {}
		for link in links.split("\n"):
			if link in Artist.ARTISTS:
				print "New link! " + link
				a_links[link] = x_data.count(link)
				print x_data.count(link)
		for link in a_links.keys():
			from_file_name = "../data/from_links/" + link.replace('/','\\') + '.txt'
			if isinstance(a_links[link], int):
				open(from_file_name,'a').write(self.name + "," + str(a_links[link]) + "\n")
		final_to_string = ["%s,%d"%(name, a_links[name]) for name in a_links.keys() if a_links[name] != "NO"]
		final_to_string = "\n".join(final_to_string)
		open(self.to_file_name,'w').write(final_to_string)
		return links

	def get_to_links(self):
		if not os.path.isfile(self.to_file_name):
			return -1
		list_form = open(self.to_file_name,'r').read().split("\n")
		if list_form == ['']:
			return {}
		if  '' in list_form:
			list_form = list_form.remove('')
		return {line.rsplit(",",1)[0]:int(line.rsplit(",",1)[1]) for line in list_form}

	def size_to_links(self):
		to_links = self.get_to_links()
		if to_links == -1:
			return 0
		return len(to_links.values())

	def get_from_links(self):
		from_file_name = "../data/from_links/" + self.name.replace('/','\\') + '.txt'
		if not os.path.isfile(from_file_name):
			return -1
		list_form = open(from_file_name,'r').read().split("\n")
		if list_form == ['']:
			return {}
		list_form.remove('')

		return {line.rsplit(",",1)[0]:int(line.rsplit(",",1)[1]) for line in list_form}

	def size_from_links(self):
		from_links = self.get_from_links()
		if from_links == -1:
			return 0
		return len(from_links.values())

	@classmethod
	def get_pops(cls):
		arr_artists = open("../data/readable/final_clean_data.txt",'r').read().split("\n")

		pop_dict = {artist: 1/float(Artist.LENGTH) for artist in arr_artists}

		for time in range(Artist.ITER):
			temp_dict = {key:pop_dict[key] for key in pop_dict.keys()}
			for artist in arr_artists:
				artist_obj = Artist(artist)
				if artist_obj.get_from_links() != -1:
					ranks = [pop_dict[link_artist] / Artist(link_artist).size_to_links() for link_artist in artist_obj.get_from_links()]
					final_pop = sum(ranks)
					temp_dict[artist] = final_pop
					print artist + ", at iteration " + str(time + 1) + ", has a popularity score of " + str(final_pop) + "."
				else:
					temp_dict[artist] = 0
					print artist + " has no incoming links. His/her/their popularity score has been set to 0."
				if time == Artist.ITER - 1:
					try:
						open(artist_obj.pop_file,'w').write(str(final_pop))
					except NameError: 
						ranks = [pop_dict[link_artist] / Artist(link_artist).size_to_links() for link_artist in artist_obj.get_from_links()]
						final_pop = sum(ranks)
						open(artist_obj.pop_file, 'w').write(str(final_pop))
			pop_dict = {key:temp_dict[key] for key in temp_dict.keys()}
		return pop_dict
	
	@classmethod
	def gen_artists(cls, artists):
		#this gets all the article data from the artists and weeds out red links that lead to missing articles
		return [Artist(artist) for artist in artists if not red(Artist(artist))]


