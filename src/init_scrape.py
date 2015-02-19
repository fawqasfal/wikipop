#coding=utf8
import requests
from BeautifulSoup import BeautifulSoup
import types
import os
import random
from cleaners import *
SIZE = 100
INIT_LIST = "Lists_of_musicians"
LIST_OF_LISTS = "../data/readable/listoflists.txt" #raw HTML data of the INIT_LIST article
SUBSET = "../data/readable/listoflists_cont.txt" #subset of the INIT_LIST, containing SIZE lists
SECTIONS = "../data/unreadable/allpages.txt" #raw xml data of the sections of the SUBSET lists
UNCLEAN = "../data/unreadable/final_data.txt" #raw data of artist names 
CLEAN = "../data/readable/final_clean_data.txt" #cleaned data of artist names
HEADER = "https://en.wikipedia.org/w/api.php?" #header string for all API calls
BANNED = ["List of fictional music groups", "List of best-selling girl groups", "music genre", "musician",
		  "Category:Lists of musicians", "Category:Lists of lists", "List of American grunge bands", "List of post-grunge bands"] 
#These articles are BANNED because they give us a significant amount of undetectable garbage.
BAD = ["List_of_musicians_from_Quebec","List_of_blues_musicians","List_of_symphony_orchestras_in_the_United_States", 
	   "List_of_musicians_who_play_left-handed", "List_of_Iranian_composers", "List_of_singer-songwriters",
	   "List_of_Carnatic_artists"]
def init_lists(article):
	#retrieves the initial list of genre lists using article with title "article" as the source. 
	#Most probably going to be "Lists of musicians"
	link = HEADER + "action=query&titles=%s&prop=revisions&rvprop=content&format=xmlfm"%article
	unformatted = (requests.get(link).text + "\n").encode('utf8')
	return unformatted


def random_sublists(size, full_lists):
	#from the string of full_lists that contains the presumably clean data for all genres, return a clean random sublist 
	full_lists = full_lists.split("\n")
	random.shuffle(full_lists)
	return "\n".join(full_lists[:size])

def article_sections(list_of_lists):
	#given string "list_of_lists" which contains the presumably clean list of articles to scan
	#return the xml data containing all the section names

	list_of_lists = list_of_lists.split("\n")
	ans = ""
	for musicians in list_of_lists:
		ans +=  (requests.get(HEADER + "action=parse&page=%s&prop=sections&format=xml"%musicians).text + "\n").encode('utf8')
		print "Got section data on " + musicians

	return ans

def raw_artists(sections):
	#gets the artists from the sections data of the random subset; given in "sections". 
	xmls = sections.split("\n")
	xmls = [BeautifulSoup(xml).sections.findAll("s") for xml in xmls if BeautifulSoup(xml).sections != None]
	print str(len(xmls)) + " good articles (contain proper sections), compared to potential " + str(SIZE) + " total."

	"""turn the raw xml data into BeautifulSoup objects. Some of the lines are blank/have no sections -- these are None. 
	The "s" portions of the BeautifulSoup sections contain the actual information needed. Some of the sections.split data
	actually just has sections of fuller articles,
	which won't work for our purposes, because sections dont have their own sections.""" 

	ans = ""
	bs = 0 #amount of "BAD SECTIONS!. see below for more"
	gs = 0 #amount of "GOOD SECTIONS!."
	state = True 
	streak = 0
	streaks = []
	#sections with heading 's' contain actual article data
	for xml in xmls: 
		for titles in xml:
			#xml contains all the xml data of one article; titles contains the data for each section of that article
			line = titles["line"] #Get the xml related to this subsection
			if titles.get("fromtitle") != None: 
				title = titles["fromtitle"]
			if  bad_section(line) or not (right_section(line) or title in BAD):
				print "BAD SECTION! " + line + " " + title
				state = False
				bs += 1
				streak += 1
				if streak > 3 and title not in streaks:
					streaks.append(title)
				continue 
				#only certain section types -- most commonly "A-Z","0-9" sections -- are sections with lists of artists in them.
			else:
				state = True
				streak = 0
			if titles["index"] == "":
				index = titles["number"]
			else:
				index = titles["index"]
			#some sections have empty "index" variables and just refer to the "number" variable for the index. dunno why.
			FOOTER = "action=query&titles=%s&prop=revisions&rvprop=content&rvsection=%s&format=xmlfm"%(title,index)
			ans += requests.get(HEADER + FOOTER).text.encode('utf8') + '\n'
			print "Finished section title '" + line + "' from " + title #eg. : "Finished C of 1970s Christian pop artists."
			gs += 1
	print str(bs) + " BAD SECTIONS!. " + str(gs) + " GOOD SECTIONS!. " + str(100 * float(bs) / float(bs + gs)) + "% are bad. "
	print "DANGEROUS ARTICLES:"
	for streak in streaks:
		print streak
	return ans

def right_section(line):
	def isAZ(c):
		return ord(c) in range(ord('A'), ord('Z') + 1)
	def low_case(c):
		return ord(c) in range(ord('a'), ord('z') + 1)
	def is09(c):
		return ord(c) in range(ord('0'), ord('9') + 1)
	def isHyph(c):
		return '-' in c or '&ndash;' in c or u'–' in c
	#determines if a certain section contains artists or other miscallaneous information
	#usually, sections that start with A-Z, 0-9 are going to contain artists who's names start with that character. 
	init = len(line) == 1
	let_range = init and isAZ(line) #gets A through Z section names
	num_range = init and is09(line) #gets 0 through 9 section names]
	end = len(line) - 1
	three_range = len(line) >= 3 and (is09(line[0]) or isAZ(line[0])) and isHyph(line[1:end]) and (is09(line[end]) or isAZ(line[end]))
	#gets A-Ls, Ms-Ns, 0-9s, etc. 
	five_range = len(line) >= 5 and isAZ(line[0]) and low_case(line[1]) and isHyph(line[2:end - 1]) and isAZ(line[end - 1]) and low_case(line[end])
	#gets Ab-Ads, Kl-Kys, etc.
	year_eq = line.isdigit() and int(line) > 1700 and int(line) < 2014 #this is years; ex.: 1955
	year_eq = year_eq or (line[:end].isdigit() and line[end] == 's' and int(line[:end]) > 1700 and int(line[:end]) < 2014)  
	#this is decades; ex. 1960s
	return let_range or num_range or three_range or five_range or year_eq


def get_data():
	folders = ["../data/to_links/", "../data/from_links/", "../data/popularity/", "../data/networks/","../data/prob/"]
	for folder in folders:
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			if os.path.isfile(file_path):
				try:
					os.unlink(file_path)
				except Exception, e:
					print e
	print "Starting the initial scraping of the list of genres to analyze."
	unclean_lists = init_lists(INIT_LIST) #Lists_of_musicians article; raw HTML
	print "Finished getting initial list"
	cleaned = clean_data(unclean_lists, BANNED) #article; cleaned for artist names
	print "Cleaned initial list"
	sublists = random_sublists(SIZE, cleaned) #random sublists from cleaned; size SIZE
	print "Got sublist"
	sections = article_sections(sublists) #section titles for all the lists in sublists
	print "Got section data"
	unclean_artists = raw_artists(sections) #uncleaned data on the artists 
	print "Got raw artist data"
	cleaned_artists = clean_data(unclean_artists, BANNED)
	final_artists = artists_filter(cleaned_artists)
	print "Got clean artist data. Starting write ..."

	amt_garbage = len(cleaned_artists.split("\n"))
	amt_clean = len(final_artists.split("\n"))
	print str(amt_garbage) + " garbage AND clean artists."
	print str(amt_clean) + " clean artists."
	print str(amt_garbage - amt_clean) + " found garbage artists." 
	print str(100 * float(amt_garbage - amt_clean) / float(amt_clean)) + "% error."

	return [cleaned, sublists, sections, unclean_artists, final_artists]


def writes(cleaned, sublists, sections, unclean_artists, final_artists):
	#Dangerous overwrite-y code! 
	open(LIST_OF_LISTS,'w').write(cleaned)
	open(SUBSET, 'w').write(sublists)
	open(SECTIONS,'w').write(sections)
	open(UNCLEAN, 'w').write(unclean_artists)
	open(CLEAN,'w').write(final_artists)
	print "Finished."

def main():
	final = get_data()
	writes(final[0], final[1], final[2], final[3], final[4])
	#Because of the way Python's GC works, these file buffers will be automatically closed at the end of the line
if __name__ == "__main__":
	main()