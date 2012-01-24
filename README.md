Fisher Innovation Wikipedia Sentence Crawler
=============
Web [http://fisherinnovation.com/](http://fisherinnovation.com/)

NOTICE: This script is for slow scans of Wikipedia articles. Be sure to keep the delay between article connections. This script isn't setup to bog down Wikipedia, rather download a couple thousand sentences of English. Read the Wikipedia documentation on Database Downloads for more information - http://en.wikipedia.org/wiki/Wikipedia:Database_download#Why_not_just_retrieve_data_from_wikipedia.org_at_runtime.3F


This Python class takes in an initial Wikipedia article URL path parses the article for viabale sentences to log as well as linages to other Wikipedia articles. Once the page has been parsed and logged to a text file (output.txt), the next page in the queue is parsed as well and so on. All logged page URL's are logged into parsedarticlelog.txt.

Example Command Line Usage: python WikipediaSentenceCrawler.py --start '/wiki/Special:Export/Jurassic_Park_(film)'
