import init_scrape
from artist import Artist
artists = Artist.gen_artists(open(init_scrape.CLEAN,'r').read().split("\n"))
TOP = 100

pops = Artist.get_pops()
ind = 0
for artist in sorted(pops, key=pops.get, reverse=True)[:TOP]:
	print "The number " +  str(ind) + " artist, " + artist + ", has a popularity of " + str(pops[artist])
	ind += 1
