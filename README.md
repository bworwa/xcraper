XCraper
=======

Xcraper is a simple, lightweight, flexible and multi-purpose (X)HTML/XML Web scraper to be used in Python solutions.

Requirements:
--------------------

* Python 2.4+ (tested on 2.7.2+)

* py-dom-xpath
    * [Official site](http://code.google.com/p/py-dom-xpath/ "py-dom-xpath official site")
    * [Documentation](http://py-dom-xpath.googlecode.com/svn/trunk/doc/index.html "py-dom-xpath documentation")

    `sudo apt-get install python-setuptools`

    `sudo easy_install py-dom-xpath`

* uTidyLib
    * [Official site](http://utidylib.berlios.de/ "uTidy official site")
    * [Documentation](http://utidylib.berlios.de/apidoc0.2/index.html "uTidy documentation")

    `sudo apt-get install python-utidylib`

Usage
-----

* Download and extract to *directory*, you should end with something like this:

    * /directory

        * /config

            * messages.xml
            * scraper.xml

        * /src

            * /core

            * main.py (Your code goes here)

* Open `/directory/config/scraper.xml` and edit your XPath queries.

* Open `/directory/src/main.py` and start coding. From `core.scraper` import `Scraper`, create a new instance of `Scraper` and run it. This translates to:

        from scraper.core import Scraper

        scraper = Scraper()

        scraper.run(url[,timestamp])

        # If a timestamp is provided, the GET request will not be sent if the
        # HEAD response says that 'last-modified' < timestamp

        print scraper.myvar

        # Where 'myvar' is the name of the query you specified in /directory/config/scraper.xml
