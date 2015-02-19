import init_scrape
import sys 
import artist

def func():
	if len(sys.argv) == 1:
		return "You need to run this script with an artist, in between quotes, as an argument."
	elif len(sys.argv) > 2:
		return "You need to run this script with only an artist as an argument."

	artists = open(init_scrape.CLEAN,'r').read().split("\n")

	inp_artist = sys.argv[1].strip('"')

	if inp_artist not in artists:
		return "Sorry, this artist is not in the database."

	fromlinks = artist.Artist(inp_artist).get_from_links()

	if fromlinks == -1 or fromlinks == {}:
		return "Sorry, this artist has no related artists."

	fromlink_arr = [artist.Artist(key) for key in fromlinks]
	fromlink_arr = sorted(fromlink_arr, key = lambda x: float(open(x.pop_file,'r').read()), reverse = True)
	fromlink_arr = [a_file.name for a_file in fromlink_arr]
	fromlink = "\n".join(fromlink_arr)
	return fromlink 



print func()