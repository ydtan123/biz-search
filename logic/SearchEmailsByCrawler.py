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
import optparse

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item
from dbs.dbapi import Business, Email, open_db
from common.utils import InputManager, EMAILRE domain_from_url

class MySpider(CrawlSpider):
    """ Crawl through web sites you specify """
    name = "myspider"

    """
    obtain start_urls, allowed_domains
    """
    #start_urls, allowed_domains = InputManager.obtainURLs()
    start_urls, allowed_domains = self.obtainURL()

    #Add our callback which will be called for every found link
    rules = [
      Rule(SgmlLinkExtractor(), follow=True, callback="searchEmail")
    ]

    def __init__(self, from='db', to='db', dbname='bizsearch',dbpwd=None, *a, **kw):
        super(MySpider, self).__init__(*a, **kw)
        self.emailList = []

        self.from = from
        self.to = to

        if from == 'db':
            self.obtainURL = InputManager.obtainURLsFromDB
        else:
            self.obtainURL = InputManager.obtainURLsFromText

        if to == 'db':
            self.dbcursor = open_db(db=dbname).cursor()
        else:
            self.f = open('results.list', 'wb')
            assert(self.f is not None, "Cannot open %s" % to)
            self.csvWriter = csv.writer(self.f, delimiter = '\t')

    def __del__(self):
        if self.to == 'db':
            close_db(self.dbcursor)
        else:
            self.f.close()

    def _write_out_one_item(self, **kwargs):
        if self.to == 'db':
            Email.insert_one_by_names(self.dbcursor, kwargs)
        else:
            items = []
            for k.v in kwargs.iteritems():
                items.append(v)
            self.csvWriter.writerow(items)
            self.f.flush()

    def searchEmail(self, response):
        """ Check a server response page (file) for possible violations """
        try:
            if 'html' in response.headers.get("content-type", "").lower():
                domaintld = domain_from_url(response.url)
                emailPattern = EMAILRE + domaintld
                data = response.body
                temp = re.findall(emailPattern, data)
                if len(temp) > 0:
                    temp = list(set(temp))

                for email in temp:
                    _write_out_one_item(address=email)

        except:
            pass

        return Item()

def parse_args()
    optparser = optparse.OptionParser()
    optparser.add_option('-i', '--from',
                         dest='from',
                         default='business',
                         help='Input of urls. If db, urls are retrieved from db. Otherwise, from a text file.'
                         )
    optparser.add_option('-o', '--to',
                         dest='to',
                         default='email',
                         help='Output of emails. If db, emails are written to db. Otherwise, to a csv file.'
                         )
    optparser.add_option('-p', '--password',
                         dest='password',
                         help='DB password'
                         )
    options, remainder = optparser.parse_args()
    return options

def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    options = parse_args()

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
    spider = MySpider(from=options.from, to=options.to)
    crawler.queue.append_spider(spider)

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"


if __name__ == '__main__':
    main()
