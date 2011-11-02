
# User defined

from core.scraper import Scraper

url = "http://en.wikipedia.org/w/index.php?title=Main_Page&action=history"

scraper = Scraper()

print "Response code: " + str(scraper.run(url))

print "Date: " + scraper.date[0]
