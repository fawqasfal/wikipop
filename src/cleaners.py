#a set of helper functions to extract data from from markup and get rid of bad data. 
START = '<extract xml:space="preserve">'

def alphanumeric(char):
	upper_case = ord(char) in range(ord('A'), ord('Z') + 1)
	lower_case = ord(char) in range(ord('a'), ord('z') + 1)
	numbers = ord(char) in range(ord('0'), ord('9') + 1)
	return (upper_case or lower_case or numbers) 

def has_alphanumeric(word):
	for char in word:
		if alphanumeric(char):
			return True
	return False

def clean_for_words(string):
	ans = [wipe_nonalpha(x) for x in string.replace("\n", " ").split(" ") if has_alphanumeric(x)]
	return ans

def wipe_nonalpha(string):
	return "".join([char for char in wipe_tags(string) if alphanumeric(char)])

def wipe_tags(string):
	ans = string
	while "<" in ans and ">" in ans:
		if (ans.index("<") < ans.index(">")):
			ans = ans.replace(ans[ans.index("<"):ans.index(">") + 1], "")
		else:
			ans = ans.replace(ans[ans.index(">"):ans.index("<") + 1], "")
	return ans

def list_in(variable, lis):
	for var in lis:
		if var in variable:
			return True
	return False

def fix_punct(line):
	bad_ones = {"&amp;":"&", "&quot;":'"', "&lt;":"<", "&gt;":">", "&nbsp;":" ", "&#039;":"'"}
	#gets rid of html punctuation issues in line
	string = line
	for bad_one in bad_ones.keys():
		string = string.replace(bad_one, bad_ones[bad_one])
	string = string.replace("&amp;","&") #do it twice because for some reason some of them have &amp;amp;
	return string

def red(artist):
	missing = '<page ns="0" title="%s" missing="" />'%(artist.name)
	return missing in artist.get_data() or START not in artist.get_data()

def bad_section(line):
	bad_names = ["See also", "References", "External links", "Contents", "Guitarists", "Left-handed with normal stringing",
	"Notes","Puppets", "Blues from India"]
	return line in bad_names

def artist_filter(artist):
	#Some articles don't follow the pattern. Manually filtering out 
	not_in = ["Image:", "File:", ".jpg", "Special:", "User:", "Category:", "http://", "meta:", "help:", "Help:", "album)"]
	not_eq = ["violin", "musician", "singer", "songwriter", "singer-songwriter", "guitar", "keyboards", "England", "vocalist"]
	for dont in not_in:
		if dont in artist:
			return False
	return artist not in not_eq

def artists_filter(artists):
	ans = [artist for artist in artists.split("\n") if artist_filter(artist)]
	return "\n".join(ans)

def clean_data(unclean, BANNED=[]):
	#cleans raw xml/html/json data from string "unclean" for just article links
	unclean = unclean.split("\n") #break it into lines
	clean = "" 
	for line in unclean:
		if "[[" not in line or "]]" not in line:
			continue #if no "[[", no links to other articles in this line. just a precondition
		line = line[line.index("[[") + 2:line.index("]]")] 
		if '|' in line:
			line = line[:line.index('|')] 
			#if '|' is in the article title, it means the line goes like [[link_name|visible_text]]. we just want the name.
		line = fix_punct(line)
		while "<span" in line:
			line = line.replace(line[line.index("<span"):line.index(">") + 1], "")
			line = line.replace("</span>","")
		if line not in clean: #dont add duplicates
			clean += line + "\n"
	init_lists = "List of 1970s Christian pop artists" in clean 
	if init_lists:
		for banned in BANNED:
			clean = clean.replace(banned + "\n","")
	clean = clean[:len(clean) - 1] #last item is always empty \n. dont want it. 
	return clean