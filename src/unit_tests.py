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

	def setUp(self):

		self.valid_URLs = ["http://www.example.com", "http://example.com", "http://test.example.com", "http://example.com/", "https://example.com/", "shttp://example.com/"]

		self.invalid_URLs = ["www.example.com", "test", "test.com", "ftp://exmple.com", "test://test.com/"]

		self.valid_identifiers = ["a", "a1", "a_a", "a_1", "_aA", "a1a", "A1a_", "_", "__", "___"]

		self.invalid_identifiers = ["1", "1a", "*a", "+a", "a*"]

		self.validation = Validation()

		self.request = Request()

		self.xpath = Xpath()

	def test_URL_validation(self):

		print "Testing /core/src/helpers/validation.validate_url"

		result = list(self.validation.validate_url(URL) for URL in self.valid_URLs)

		self.assertEqual(result, list(True for index in range(len(self.valid_URLs))))

		result = list(self.validation.validate_url(URL) for URL in self.invalid_URLs)

		self.assertEqual(result, list(False for index in range(len(self.invalid_URLs))))

	def test_identifier_validation(self):

		print "Testing /core/src/helpers/validation.validate_identifier"

		result = list(self.validation.validate_identifier(identifier) for identifier in self.valid_identifiers)

		self.assertEqual(result, list(True for index in range(len(self.valid_identifiers))))

		result = list(self.validation.validate_identifier(identifier) for identifier in self.invalid_identifiers)

		self.assertEqual(result, list(False for index in range(len(self.invalid_identifiers))))

	def test_request_knock(self):

		print "Testing /core/src/helpers/request.knock..."

		result = self.request.knock("test", "http://en.wikipedia.org/w/index.php?title=Main_Page&action=history", True)

		self.assertTrue(result)

		result = self.request.knock("test", "http://www.google.co.ve")

		self.assertTrue(result)

		result = self.request.knock("test", "http://en.wikipedia.org/w/index.php?title=Main_Page&action=history")

		self.assertFalse(result)

		result = self.request.knock("test", "http://www.python.org/webstats/")

		self.assertFalse(result)

		result = self.request.knock("test", "http://www.google.co.ve", False, 0, 408)

		self.assertTrue(result)

		self.request.knock("test", "http://www.whitehouse.gov")

		self.assertEqual(self.request.crawl_delay, 10)

		self.request.crawl_delay = 1

	def test_request_make(self):

		print "Testing /core/src/helpers/request.make..."

		result = self.request.make("http://www.google.co.ve", "HEAD", "test", "utf8")

		self.assertEqual(self.request.current_headers == {}, False)

		self.assertEqual(self.request.current_content == "<_/>", True)

		try:

			result = self.request.make("http://www.ciens.ucv.ve", "HEAD", "test", "utf8", 404)

		except ResponseCodeError as status:

			self.assertEqual(int(str(status)), 404)

		result = self.request.make("http://www.iac.es/img/prensa/prensa519_562.jpg", "GET", "test", "utf8")

		self.assertEqual(self.request.current_content == "<_/>", True)

		result = self.request.make("http://www.ciens.ucv.ve/ciencias/", "GET", "test", "utf8")

		self.assertIsNot(self.request.current_content, "<_/>")

		self.assertIsNot(self.request.current_content.strip(), "")

		result = self.request.make("http://www.forosdelweb.com", "GET", "test", "utf8")

		self.assertEqual(self.request.current_charset, "latin1")

	def test_messages_and_log(self):

		print "Testing /core/src/messages... and /core/src/helpers/log"

		try:
		
			messages = Messages(None, "/")

		except SystemExit:

			pass

		try:
		
			messages = Messages("test")

		except SystemExit:

			pass

		try:
		
			messages = Messages("<test></test>")

		except SystemExit:

			pass

		try:
		
			messages = Messages("<messages></messages>")

		except SystemExit:

			pass

		try:
		
			messages = Messages("<messages><message></message></messages>")

		except SystemExit:

			pass

		try:
		
			messages = Messages("<messages><message name=\"test\"></message></messages>")

		except SystemExit:

			pass

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

		doc = minidom.parseString("<html><head>test</head><body><ul><li>1</li><li>2</li></ul></body></html>")

		result = []

		self.xpath.find("/html", doc, False, "utf8", result)

		self.assertEqual(result, ["<html><head>test</head><body><ul><li>1</li><li>2</li></ul></body></html>"])

		result = []

		self.xpath.find("//ul", doc, False, "utf8", result)

		self.assertEqual(result, ["<ul><li>1</li><li>2</li></ul>"])

		result = ["<li>0</li>"]

		self.xpath.find("//ul/li", doc, False, "utf8", result)

		self.assertEqual(result, ["<li>0</li>", "<li>1</li>", "<li>2</li>"])

		result = ["0"]

		self.xpath.find("/html/body/ul/li", doc, True, "utf8", result)

		self.assertEqual(result, ["0", "1", "2"])

		result = ["0"]

		self.xpath.find("/html/body/ul/li[1]", doc, True, "utf8", result)

		self.assertEqual(result, ["0", "1"])

		result = []

		self.xpath.find("/html/body", doc, True, "utf8", result)

		self.assertEqual(result, ["12"])

	def test_scraper(self):

		try:

			scraper = Scraper(None, "/")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("test")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent></user_agent></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset></charset></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>test</charset></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath></xpath></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries></queries></xpath></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"></queries></xpath></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query></query></queries></xpath></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query name=\"name\"></query></queries></xpath></scraper>")

		except SystemExit:

			pass

		try:
		
			scraper = Scraper("<scraper><general><user_agent>test</user_agent><charset>utf8</charset></general><xpath><queries hosts=\"empty\"><query name=\"name\">test</query></queries></xpath></scraper>")

		except SystemExit:

			pass

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
