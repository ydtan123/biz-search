'''
Created on Dec 1, 2011
 
    This is a crawler for seeking email address on sites.
 
@author: zul110
'''


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.item import Item
#from scrapy.http import Request
#import StringIO

#import pdb
import commands
#import sys
import csv
import tldextract
import re


FILES_PREFIX = 'YahooList'
FILES_PATH = '/Users/zul110/work3/BusinessList/Hotels/'

EMAILRE = '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z.]*'

def getFileList():
    fileList = []
    if FILES_PREFIX:
        res = commands.getstatusoutput('ls ' + FILES_PATH + FILES_PREFIX + '*')
        if res[0] == 0:
            for file in res[1].split('\n'):
                fileList.append(FILES_PATH + file.split('/')[-1])
    return fileList

def obtainURLs():
    #pdb.set_trace()
    urlList = []
    domainList = []
    fileList = getFileList()
    for fileName in fileList:
        try:
            f = open(fileName, 'rb')
            csvReader = csv.reader(f, delimiter = '\t')
            for row in csvReader:
                if row[1]:
                    theURL = row[1]
                    urlList.append(row[1])
                    ext = tldextract.extract(theURL)
                    domaintld = ext.domain + '.' + ext.tld
                    domainList.append(domaintld)
                    
        except:
            continue
    
    domainList = list(set(domainList))
    return urlList, domainList



class MySpider(CrawlSpider):
    """ Crawl through web sites you specify """
    
    name = "mycrawler"

    start_urls, allowed_domains = obtainURLs()

    #start_urls = ['http://www.dctrekker.com/', 'http://hiltongardeninn.hilton.com/en/gi/hotels/index.jhtml?ctyhocn=DCANMGI']
    #allowed_domains = ['dctrekker.com', 'hilton.com']   
    
    # Add our callback which will be called for every found link
    rules = [
        Rule(SgmlLinkExtractor(allow=('\.html',)), follow=True, callback="searchEmail")
    ]
    
    crawl_count = 0
    email_Found = 0
    
    
    def __init__(self, *a, **kw):
        super(MySpider, self).__init__(*a, **kw)
        self.emailList = []
        self.f = open('aaa', 'wb')
        self.csvWriter = csv.writer(self.f, delimiter = '\t')
        
        print MySpider.start_urls
        print MySpider.allowed_domains
        
        self.WSemailList = []
        self.WScurrDomain = ''
      
   
        
    def searchEmail(self, response):
        """ search email in the response data """
        theURL = response.url
        ext = tldextract.extract(theURL)
        domaintld = ext.domain + '.' + ext.tld
                  
        if domaintld != self.WScurrDomain:
            if self.WSemailList:
                """finish a domain"""
                self.csvWriter.writerow([self.WScurrDomain, self.WSemailList])
                self.f.flush()
                #reset                    
                self.WSemailList = []
                self.WScurrDomain = domaintld
            
        if 'html' in response.headers.get("content-type", "").lower():
            """start search the context"""              
            emailPattern = EMAILRE + domaintld
            data = response.body
            temp = re.findall(emailPattern, data) 
            if len(temp) > 0:  
                temp = list(set(temp))
                for email in temp:
                    self.WSemailList.append(email)
                    
        return Item()

   
    def _requests_to_follow(self, response):

        if getattr(response, "encoding", None) != None:
            # Server does not set encoding for binary files
            # Do not try to follow links in
            # binary data, as this will break Scrapy
            return CrawlSpider._requests_to_follow(self, response)
        else:
            return []
            
    

        
