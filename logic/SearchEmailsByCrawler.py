'''
Created on Oct 8, 2011

Search Business from Yahoo Local Search API
Generate csv files.

Load to MySQ:
    load data local infile 'uniq.csv' into table tblUniq
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    (uniqName, uniqCity, uniqComments)

@author: zul110
'''

import urlparse
import urllib2
from pyquery import PyQuery
import sys
import csv
import tldextract
import re
from sets import Set


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item
from dbs.dbapi import Business, Email, open_db

DBNAME = "biz-search"
DBUSER = "aaaa"
DBPWD = "bbbb"
DBSERVER = "192.168.0.102"

EMAILRE = '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z.]*'




class InputManager(object):

    @classmethod
    def _domain_from_url(cls, url):
        ext = tldextract.extract(url)
        return ext.domain + '.' + ext.tld

    @classmethod
    def obtainURLs(cls):
        """
        obtain unscanned URLs from business table.
        """
        urlList = ["http://www.ac-baidu.com"]
        domainList = ["ac-baidu.com"]
        return urlList, domainList

    @classmethod
    def obtainURLsFromFiles(fileList):
        """
        obtain unscanned URLs from business table.
        """
        urlList = []
        domainList = []
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

        urlList = 'http://www.yahoo.com'
        domainList = 'yahoo.com'
        return urlList, domainList


    @classmethod
    def obtainURLsFromDB(cls):
        """
        obtain unscanned URLs from business table.
        """
        with open_db(dbname='bizsearch') as bizdb:
            dbitems = Business.fetch_by(bizdb, ['url', 'country'], "country='US'")
            url_list = [ url for url,_ in dbitems ]
            domain_list = [ cls._domain_from_url(d) for d in url_list ]
        print url_list
        print domain_list
        return url_list, domain_list

class MySpider(CrawlSpider):
    """ Crawl through web sites you specify """
    name = "myspider"

    """
    obtain start_urls, allowed_domains
    """
    #start_urls, allowed_domains = InputManager.obtainURLs()
    start_urls, allowed_domains = InputManager.obtainURLsFromDB()

    #Add our callback which will be called for every found link
    rules = [
      Rule(SgmlLinkExtractor(), follow=True, callback="searchEmail")
    ]

    def __init__(self, *a, **kw):
        super(MySpider, self).__init__(*a, **kw)
        self.emailList = []
        self.f = open('aaa', 'wb')
        self.csvWriter = csv.writer(self.f, delimiter = '\t')


    def searchEmail(self, response):
        """ Check a server response page (file) for possible violations """
        try:
            if 'html' in response.headers.get("content-type", "").lower():
                theURL = response.url
                ext = tldextract.extract(theURL)
                domaintld = ext.domain + '.' + ext.tld

                emailPattern = EMAILRE + domaintld
                data = response.body
                temp = re.findall(emailPattern, data)
                if len(temp) > 0:
                    temp = list(set(temp))

                for email in temp:
                    self.csvWriter.writerow([email, domaintld])
                    self.f.flush()
                    print email, domaintld
                    with open_db("bizsearch") as emaildb:
                        Email.insert_one_by_names(emaildb, address=email)
        except:
            pass

        return Item()




def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # shut off log
    from scrapy.conf import settings
    settings.overrides['LOG_ENABLED'] = True
    settings.overrides['DEPTH_LIMIT'] = 2


    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    spider = MySpider()
    crawler.queue.append_spider(spider)

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"


if __name__ == '__main__':
    main()
