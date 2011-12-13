'''
Created on Dec 1, 2011
 
    This is a crawler for seeking email address on sites.
 
@author: zul110
'''


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.selector import HtmlXPathSelector

from scrapers.common.items import BizItem 
from scrapers.common import utils

class HotelBaseScraper(CrawlSpider):
    """ Crawl through web sites you specify """
    
    name = "hotelbase_scraper"

    start_urls, allowed_domains = obtainURLsFromText()

    #allowed_domains = ['dctrekker.com', 'hilton.com']   
    
    # Add our callback which will be called for every found link
    rules = [
        Rule(SgmlLinkExtractor(allow=('\.html',)), follow=True, callback="searchEmail")
    ]
    
    def __init__(self, *a, **kw):
        super(HotelBaseSpider, self).__init__(*a, **kw)
    
    def searchHotels(self, response):
        """search hotels in hotel-base.com"
        item = BizItem()
        hxs = HtmlXPathSelector(response)
        cities = hxs.select("//table[@class='cTx fA11n']")
        for city in cities:
            biz = city.select("")
            for b in biz:
                item['name'] = ""
                item['url'] = ""
                item['phone'] = ""
                item['addr']= ""
                yield item

    def _requests_to_follow(self, response):

        if getattr(response, "encoding", None) != None:
            # Server does not set encoding for binary files
            # Do not try to follow links in
            # binary data, as this will break Scrapy
            return CrawlSpider._requests_to_follow(self, response)
        else:
            return []
            
    

        
