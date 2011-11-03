
# User defined

from core.scraper import Scraper

url = "http://en.wikipedia.org/wiki/index.php?title=Main_Page&action=history"

scraper = Scraper()

print "Response code: " + str(scraper.run(url))

try:

	# Your code goes here

	print "Date: " + scraper.date[0]

except AttributeError as message:

	print message
