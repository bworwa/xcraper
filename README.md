XCraper
=======

Xcraper is a simple, lightweight, flexible and multi-purpose (X)HTML/XML Web scraper to be used in Python solutions.

Requirements
------------

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

        * /config (*Your app. configuration files goes here*)

            * messages.xml
            * scraper.xml

        * /src

            * /core (*Don't edit this if you don't have to*)

            * main.py (*Your code goes here*)

* Open `/directory/config/scraper.xml` and edit your XPath queries.

    XPath queries are defined in the `queries` tag as a `query` tag. Each `query` tag must be defined as follows:

    `<query name="name" [context="context" get_value="bool"]>XPath query</query>`

    `name` must be a valid and unique [Python identifier](http://docs.python.org/reference/lexical_analysis.html#identifiers "Python identifier"). This attribute is mandatory.

    `context` must be a **previously defined** `name`. This attribute is optional and defines where the XPath query will be evaluated.

       If the attribute `context` is not present or it's value is `none`, the XPath query will be evaluated in the entire (X)HTML/XML document. Otherwise it'll be evaluated only in the resulting (X)HTML/XML node(s) of the specified context.

       E.g:

            <query name="a">//ul</query>
            <query name="b" context="a">/ul/li</query>

            'a' will return all the 'ul' elements found in the entire (X)HTML/XML document
            'b' will return all the 'li' elements found in the 'ul' elements returned by 'a'

       All the results are treated like lists, so if

            'a' returns ['<ul>...</ul>', '<ul>...</ul>', '<ul>...</ul>']

       Then

            'b' returns [['<li>...</li>'], ['<li>...</li>', '<li>...</li>'], [None]]

       Note that if no match is found, `None` will be returned in order to maintain the lists integrity.
     
     
    `get_value` must be either `true` or `false` (default is `false`). This attribute is optional and specifies whether to get the entire node or just the text value of the node.

       E.g:

            <query name="a">//ul</query>
            <query name="b" context="a" get_value="true">/ul/li</query>

            'b' returns [['item 1'], ['item 2', 'item 3'], [None]]

            instead of

            [['<li>item 1</li>'], ['<li>item 2</li>', '<li>item 3</li>'], [None]]

* Open `/directory/src/main.py` and start coding!. From `core.scraper` import `Scraper`, create a new instance of `Scraper` and run it. This translates to:

        from core.scraper import Scraper

        scraper = Scraper()

        scraper.run(url[,timestamp])

        print scraper.myvar


    `timestamp` is an optional parameter that tells the scraper to ignore `url` if the header `last-modified` is lower than `timestamp`. In this case, only a `HEAD` request will be made, skipping the `GET` request and saving you some time.

    If no `timestamp` is specified, it is defaulted to `0` forcing the `GET` request.

    `myvar` is the `name` of the query specified in `/directory/config/scraper.xml` and it'll contain the XPath query result.

    So, assuming the following query

        <query name="price" get_value="true">//span[@id='price']</query>

    applied to an imaginary markup with a `<span id="price">$99.99</price>`,

    if we print `scraper.price` we get `['$99.99']`

Customization
-------------

You can add your own custom messages in `directory/config/messages.xml` or even replace the existing ones.

To add a message simply add a new `message` tag inside the `messages` tag. Each message tag must have a `name` attribute, which behaves identically to the `name` attribute of the `query` tag.

Then you can import `Messages` from `core.messages` and use your custom messages.

E.g: (in `directory/config/messages.xml`) add

        <message name="usr_input_error">Wrong input value '%(input_value)s'</message>

And in your code

        from core.messages import Messages
    
        messages = Messages()

        print messages.USR_INPUT_ERROR % { "input_value" : var }

You can also raise errors 

        messages.raise_error(msg[, section="scraper", log_it = True])

issue warnings

        messages.issue_warning(msg[, section="scraper", log_it = True])

and inform

        messages.inform(msg[, new_line = True, section="scraper", log_it = True])

Raising an error will stop the program's execution, issuing warnings won't.

`msg` is just a `string` containing the error or warning explanation. 

`section` is a `string` that defines in which sub-directory of `/directory/logs` the error or warning will be logged. You can use `messages.SCRAPER` or `messages.INTERNAL` to log errors in the `scraper` or `internal` sub-directories respectively. Default section is `scraper`.

`log_it` specifies whether the error should be logged or not. Default value is `True`.

inform's `new_line` specifies if the message will end with a line break (`\n`). Default value is `True`.

