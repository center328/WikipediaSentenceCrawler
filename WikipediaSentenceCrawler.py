#!/usr/bin/python

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

class WikipediaSentenceCrawler(object):
    BASE_URL = 'http://en.wikipedia.org'
    ARTICLES_TO_LOOKUP = []
    ARTICLES_PARSED = []
    MAX_QUEUE_SIZE = 10
    
    
    def __init__(self):
        print "Fisher Innovation Wikipedia Sentence Crawler"
        print "Written By: Matt Fisher"
        print "Web: http://www.fisherinnovation.com"
        print "--------------------------------------------"
        print ""
        

    ##
    # Starts the parser.
    #
    # @param url:    The /wiki/* URL of the initial article.
    ##
    def startParser(self, url):
        # Save the initial article
        self.ARTICLES_TO_LOOKUP.append(url)
        self.loop()
        
    
    ##
    # Loop until we learn everything!
    ##
    def loop(self):
        url = self.ARTICLES_TO_LOOKUP.pop()
        self.ARTICLES_PARSED.append(url)
        self.logParsedArticle(url)
        self.parseArticleLinks(url)
        self.parseArticle(url)
        print '>> NOTICE: ' + str(len(self.ARTICLES_PARSED)) + ' Articles parsed.'
    
        self.loop()
    
    
    ##
    # Fetches a Wikipedia article and returns the clean 
    # article data sentences.
    #
    # @param url:    The Wikipedia URL to lookup.
    ##
    def parseArticle(self, url):
        print '>> NOTICE: Attempting to parse ' + str(url)
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(self.BASE_URL + url)
        page = infile.read()
        soup = BeautifulSoup(page)
        data = soup.findAll('p') 
        
        for n in data:
            if len(n) > 1:
                self.exportArticleToTextFile(self.remove_html_tags(str(n)))
            else:
                print ">> NOTICE: Ignoring parsed paragraph, input too short."
        
    
    ##
    # Exports a stricle text to a text file.
    #
    # @param text:    The article text to appent to the text file.
    ##
    def exportArticleToTextFile(self, text):
        print '>> NOTICE: Logging: ' + text
        
        try:
            # This tries to open an existing file but creates a new file if necessary.
            logfile = open("output.txt", "a+")
            try:
                logfile.write(text + "\n")
            finally:
                logfile.close()
        except IOError:
            pass
        
        
    ##
    # Logs the parsed article URL to a text file.
    #
    # @param url:    The parsed article url.
    ##
    def logParsedArticle(self, url):
        try:
            # This tries to open an existing file but creates a new file if necessary.
            logfile = open("parsedarticlelog.txt", "a+")
            try:
                logfile.write(url + "\n")
            finally:
                logfile.close()
        except IOError:
            pass
    
    
    ##
    # Removes all HTML tags from a string.
    #
    # @param data:    The string with HTML elements in it.
    ##
    def remove_html_tags(self, data):
        p = re.compile(r'<[^<]*?>')
        return p.sub('', data)
    
    
    ##
    # Finds all the local links to other Wikipedia Articles in the 
    # given Wikipedia URL. 
    #
    # @param url:    The Wikipedia URL to lookup.
    ##
    def parseArticleLinks(self, url):
        global ARTICLES_TO_LOOKUP
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(self.BASE_URL + url)
        response = infile.read()
        
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                # Verify local link
                testlink = link['href']
                
                if "/wiki/" in testlink:
                    if not "//" in testlink: 
                        if not ":" in testlink: 
                            if not "Main_Page" in testlink:
                                if not "Wikimedia_Foundation" in testlink:
                                    # Only add new articles to the queue
                                    if self.verifyNewArticle(testlink):
                                        #print 'Adding new article to queue: ' + testlink
                                        if len(self.ARTICLES_TO_LOOKUP) < self.MAX_QUEUE_SIZE:
                                           self.ARTICLES_TO_LOOKUP.append(testlink)
        
        print '>> NOTICE: ' + str(len(self.ARTICLES_TO_LOOKUP)) + ' Articles in crawler queue.'
    
    
    ##
    # Checks if this article has been logged or queued yet. 
    #
    # @param url:    The Wikipedia URL to verify.
    ##
    def verifyNewArticle(self, url):
        for n in self.ARTICLES_TO_LOOKUP:
            if n == url:
                return False
        
        for n in self.ARTICLES_PARSED:
            if n == url:
                return False
        
        return True
    

# Starting at the Jurassic Park article.
n = WikipediaSentenceCrawler()   
n.startParser('/wiki/Jurassic_Park_(film)')