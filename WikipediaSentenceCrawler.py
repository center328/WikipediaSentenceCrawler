#!/usr/bin/python

import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import string
import os

__appname__ = "[Fisher Innovation Wikipedia Senetence Crawler]"
__author__  = "Matt Fisher (fisher.matt@gmail.com)"
__version__ = "0.3 alpha"
__license__ = ""


class WikipediaSentenceCrawler(object):
    # Configuration
    BASE_URL = 'http://en.wikipedia.org'
    STRIP_PUNCTUATION = True
    ALL_LOWER_CASE = True
    CONVERT_NUMBERS_TO_WORDS = True

    
    ARTICLES_TO_LOOKUP = []
    ARTICLES_PARSED = []
    MAX_QUEUE_SIZE = 10
    SENTENCE_LOG_COUNT = 0
    WORD_COUNT = 0
    KILL = False

    ones = ["", "one ","two ","three ","four ", "five ",
        "six ","seven ","eight ","nine "]
    
    tens = ["ten ","eleven ","twelve ","thirteen ", "fourteen ",
        "fifteen ","sixteen ","seventeen ","eighteen ","nineteen "]
    
    twenties = ["","","twenty ","thirty ","forty ",
        "fifty ","sixty ","seventy ","eighty ","ninety "]
    
    thousands = ["","thousand ","million ", "billion ", "trillion ",
        "quadrillion ", "quintillion ", "sextillion ", "septillion ","octillion ",
        "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ",
        "quattuordecillion ", "sexdecillion ", "septendecillion ", "octodecillion ",
        "novemdecillion ", "vigintillion "]
    
    
    ##
    #
    ##
    def __init__(self):
        print ""
        print "_______________________________________________________________________"
        print "           Fisher Innovation Wikipedia Sentence Crawler"
        print "          Created By: Matt Fisher (fisher.matt@gmail.com)"
        print "              Web: http://www.fisherinnovation.com"
        print " Source: https://github.com/fisherinnovation/WikipediaSentenceCrawler"
        print "_______________________________________________________________________"
        print ""
        

    ##
    # Starts the parser.
    #
    # @param url:    The /wiki/* URL of the initial article.
    ##
    def startParser(self, url):
    	print '>> NOTICE: Attemping initial connection to ' + self.BASE_URL + url
    	
        self.KILL = False
        
        # Save the initial article
        self.ARTICLES_TO_LOOKUP.append(url)
        self.loop()
        
        
    ##
    # Stops the parser if running.
    ##
    def stopParser(self):
        self.KILL = True
        
    
    ##
    # Loop until we learn everything!
    ##
    def loop(self):
        if self.KILL:
            return
        
        url = self.ARTICLES_TO_LOOKUP.pop()
        self.ARTICLES_PARSED.append(url)
        self.logParsedArticle(url)
        self.parseArticleLinks(url)
        self.parseArticle(url)
        
        print '>> NOTICE: ' + str(len(self.ARTICLES_PARSED)) + ' Articles Parsed. ' + str(self.SENTENCE_LOG_COUNT) + ' Sentences Logged. ' + str(self.WORD_COUNT) + ' Words Logged.'
    	
    	outputsize = self.convertBytes(os.path.getsize("output.txt"))
    	articlelogsize = self.convertBytes(os.path.getsize("parsedarticlelog.txt"))
    	
    	print '>> NOTICE: Sentence Log Filesize: ' + str(outputsize) + '. Parsed Article Log Filesize: ' + str(articlelogsize) + '.'
        
        self.loop()
    
    
    ##
    # Converts bytes to cleaner output.
    #
    # @param bytes: The amount of bytes to convert
    ##
    def convertBytes(self, bytes):
        bytes = float(bytes)
        
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2fTB' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2fGB' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2fMB' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2fKB' % kilobytes
        else:
            size = '%.2fb' % bytes
        
        return size
    
    
    ##
    # Fetches a Wikipedia article and returns the clean 
    # article data sentences.
    #
    # @param url:    The Wikipedia URL to lookup.
    ##
    def parseArticle(self, url):
        print '>> NOTICE: Attempting to fetch ' + str(url)
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open(self.BASE_URL + url)
        page = infile.read()
        
        print '>> NOTICE: ' + url + ' recieved! Starting article parsing...'
        
        soup = BeautifulSoup(page)
        data = soup.findAll('p') 
        
        for n in data:
            if len(n) > 10:
                pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
                results = pat.findall(self.remove_html_tags(str(n)))
                
                for m in results:
                    if len(m) > 50:
                        if self.STRIP_PUNCTUATION:
                            m = m.translate(None, string.punctuation)
                            
                        if self.ALL_LOWER_CASE:
                            m = str.lower(str(m))
                            
                        if self.CONVERT_NUMBERS_TO_WORDS:
                            p = m.split(' ')
                            n = ''
                            for w in p:
                                if w.isdigit():
                                    w = self.intToString(w)
                                    w = w[:-1] 
                                    
                                n = n + w + ' '
                                m = n
                        
                        # Update word count
                        c = m.split(' ')
                        for w in c:
                         	self.WORD_COUNT = self.WORD_COUNT + 1
                                
                        self.SENTENCE_LOG_COUNT = self.SENTENCE_LOG_COUNT + 1
                        self.exportArticleToTextFile(m)
            else:
                #print ">> NOTICE: Ignoring parsed paragraph, input too short."
                pass
        
    
    ##
    # Exports a stricle text to a text file.
    #
    # @param text:    The article text to appent to the text file.
    ##
    def exportArticleToTextFile(self, text):
        #print '>> NOTICE: Logging: ' + text
        
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
        
        for link in BeautifulSoup(response, fromEncoding="latin1", parseOnlyThese=SoupStrainer('a')):
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
    
    
    ##
    # Integer number to english word conversion
    # can be used for numbers as large as 999 vigintillion
    # (vigintillion --> 10 to the power 60)
    #
    # @param n:    The int to convert to string.
    ##
    def intToString(self, n):
        n3 = []
        r1 = ""
        ns = str(n)
        for k in range(3, 33, 3):
            r = ns[-k:]
            q = len(ns) - k
            # break if end of ns has been reached
            if q < -2:
                break
            else:
                if  q >= 0:
                    n3.append(int(r[:3]))
                elif q >= -1:
                    n3.append(int(r[:2]))
                elif q >= -2:
                    n3.append(int(r[:1]))
            r1 = r
        
        nw = ""
        for i, x in enumerate(n3):
            b1 = x % 10
            b2 = (x % 100)//10
            b3 = (x % 1000)//100
            
            if x == 0:
                continue
            else:
                t = self.thousands[i]
            if b2 == 0:
                nw = self.ones[b1] + t + nw
            elif b2 == 1:
                nw = self.tens[b1] + t + nw
            elif b2 > 1:
                nw = self.twenties[b2] + self.ones[b1] + t + nw
            if b3 > 0:
                nw = self.ones[b3] + "hundred " + nw
            
        return nw
    


##   
# Validates argument inputs.
##
def validateArguments():
    # Article Source
    if opts.start == False:
        print "ERROR: No start article supplied. --start"
        return
    else: 
    	if len(args) > 0:
        	n = WikipediaSentenceCrawler()   
         	n.startParser(args[0])
        else:
        	print "ERROR: No start article supplied. --start"
        	return
        
    
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description=__doc__, version="%%prog v%s" % __version__)
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose", default=False, help="Increase verbosity")
    parser.add_option('-s', '--start', action="store_true", dest="start", help="Starting article")
    
    opts, args = parser.parse_args()
	
    validateArguments()