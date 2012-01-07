import unittest, sys

from core.helpers.validation import Validation
from core.helpers.request import Request, ResponseCodeError
from core.helpers.custom_xpath import Xpath
from core.messages import Messages
from core.scraper import Scraper

from datetime import datetime
from os.path import dirname, abspath
from xml.dom import minidom

class Test(unittest.TestCase):

	def test_URL_validation(self):

		#self.skipTest("Timewise")

		print "Testing /core/src/helpers/validation.validate_url"

		valid_URLs =	["http://www.example.com",
				"http://example.com",
				"http://test.example.com",
				"http://example.com/",
				"https://example.com/",
				"shttp://example.com/"]

		invalid_URLs = ["www.example.com",
				"test", "test.com",
				"ftp://exmple.com",
				"test://test.com/"]

		validation = Validation()

		result = list(validation.validate_url(URL) for URL in valid_URLs)

		self.assertEqual(result, list(True for index in range(len(valid_URLs))))

		result = list(validation.validate_url(URL) for URL in invalid_URLs)

		self.assertEqual(result, list(False for index in range(len(invalid_URLs))))

	def test_identifier_validation(self):

		#self.skipTest("Timewise")

		print "Testing /core/src/helpers/validation.validate_identifier"

		valid_identifiers = ["a", "a1", "a_a", "a_1", "_aA", "a1a", "A1a_", "_", "__", "___"]

		invalid_identifiers = ["1", "1a", "*a", "+_a_", "a*"]

		validation = Validation()

		result = list(validation.validate_identifier(identifier) for identifier in valid_identifiers)

		self.assertEqual(result, list(True for index in range(len(valid_identifiers))))

		result = list(validation.validate_identifier(identifier) for identifier in invalid_identifiers)

		self.assertEqual(result, list(False for index in range(len(invalid_identifiers))))

	def test_request_knock(self):

		#self.skipTest("Timewise")

		print "Testing /core/src/helpers/request.knock..."

		request = Request()

		result = request.knock("test", "http://en.wikipedia.org/w/index.php?title=Main_Page&action=history", True)

		self.assertTrue(result)

		result = request.knock("test", "http://www.google.co.ve")

		self.assertTrue(result)

		result = request.knock("test", "http://en.wikipedia.org/w/index.php?title=Main_Page&action=history")

		self.assertFalse(result)

		result = request.knock("test", "http://www.python.org/webstats/")

		self.assertFalse(result)

		result = request.knock("test", "http://www.google.co.ve", False, 0, 408)

		self.assertTrue(result)

		request.knock("test", "http://www.whitehouse.gov")

		self.assertEqual(request.crawl_delay, 10)

		request.crawl_delay = 1

	def test_request_make(self):

		#self.skipTest("Timewise")

		print "Testing /core/src/helpers/request.make..."

		request = Request()

		result = request.make("http://www.google.co.ve", "HEAD", "test", "utf8")

		self.assertEqual(request.current_headers == {}, False)

		self.assertEqual(request.current_content == "<_/>", True)

		try:

			result = request.make("http://www.ciens.ucv.ve", "HEAD", "test", "utf8", 404)

		except ResponseCodeError as status:

			self.assertEqual(int(str(status)), 404)

		result = request.make("http://www.iac.es/img/prensa/prensa519_562.jpg", "GET", "test", "utf8")

		self.assertEqual(request.current_content == "<_/>", True)

		result = request.make("http://www.ciens.ucv.ve/ciencias/", "GET", "test", "utf8")

		self.assertIsNot(request.current_content, "<_/>")

		self.assertIsNot(request.current_content.strip(), "")

		result = request.make("http://www.forosdelweb.com", "GET", "test", "utf8")

		self.assertEqual(request.current_charset, "latin1")

	def test_messages_and_log(self):

		#self.skipTest("Timewise")

		print "Testing /core/src/messages... and /core/src/helpers/log"

		count = 0

		try:
		
			messages = Messages(None, "/")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("test")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("<_/>")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("<test></test>")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("<messages></messages>")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("<messages><message></message></messages>")

		except SystemExit:

			count += 1

		try:
		
			messages = Messages("<messages><message name=\"test\"></message></messages>")

		except SystemExit:

			count += 1

		self.assertEqual(count, 7)

		messages = Messages("<messages><message name=\"test\">test</message></messages>")

		messages.TEST

		now = datetime.now()

		open(dirname(dirname(abspath(__file__))) + "/logs/internal/%d-%d-%d.log" % (now.day, now.month, now.year))

		messages.issue_warning("test")

		open(dirname(dirname(abspath(__file__))) + "/logs/scraper/%d-%d-%d.log" % (now.day, now.month, now.year))

		messages.inform("test", True, "test", False)

		try:

			open(dirname(dirname(abspath(__file__))) + "/logs/test/%d-%d-%d.log" % (now.day, now.month, now.year))

		except IOError:

			pass

		messages.inform("test", True, "test", True)

		open(dirname(dirname(abspath(__file__))) + "/logs/test/%d-%d-%d.log" % (now.day, now.month, now.year))

	def test_custom_xpath(self):

		#self.skipTest("Timewise")

		xpath = Xpath()

		doc = minidom.parseString("<html><head>test</head><body><ul><li>1</li><li>2</li></ul></body></html>")

		result = []

		xpath.find("/html", doc, False, "utf8", result)

		self.assertEqual(result, ["<html><head>test</head><body><ul><li>1</li><li>2</li></ul></body></html>"])

		result = []

		xpath.find("//ul", doc, False, "utf8", result)

		self.assertEqual(result, ["<ul><li>1</li><li>2</li></ul>"])

		result = ["<li>0</li>"]

		xpath.find("//ul/li", doc, False, "utf8", result)

		self.assertEqual(result, ["<li>0</li>", "<li>1</li>", "<li>2</li>"])

		result = ["0"]

		xpath.find("/html/body/ul/li", doc, True, "utf8", result)

		self.assertEqual(result, ["0", "1", "2"])

		result = ["0"]

		xpath.find("/html/body/ul/li[1]", doc, True, "utf8", result)

		self.assertEqual(result, ["0", "1"])

		result = []

		xpath.find("/html/body", doc, True, "utf8", result)

		self.assertEqual(result, ["12"])

	def test_scraper(self):

		#self.skipTest("Timewise")

		count = 0

		try:

			scraper = Scraper(None, "/")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("test")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<_/>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent></user_agent></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset></charset></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>test</charset></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath></xpath></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries></queries></xpath></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"></queries></xpath></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query></query></queries></xpath></scraper>")

		except SystemExit:

			count += 1

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query name=\"name\"></query></queries></xpath></scraper>")

		except SystemExit:

			count += 1

		scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query name=\"name\">test</query></queries></xpath></scraper>")

		self.assertEqual(count, 15)

		self.assertEqual(scraper.config["user_agent"], "test")

		self.assertEqual(scraper.config["charset"], "utf8")

		scraper = Scraper()

		result = scraper.run("http://www.google.co.ve")

		self.assertEqual(result, False)

		result = scraper.run("http://en.wikipedia.org/wiki/Justus")

		self.assertEqual(result, 301)

		result = scraper.run("http://en.wikipedia.org/w/index.php?title=Justus&action=history", 1577858400)

		self.assertEqual(result, False)

		result = scraper.run("http://en.wikipedia.org/w/index.php?title=Justus&action=history")

		self.assertEqual(result, 200)

		scraper.revision

if __name__ == "__main__":

	unittest.main()
