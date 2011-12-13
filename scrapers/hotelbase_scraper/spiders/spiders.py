'''
Created on Dec 10, 2011

    This is a crawler for seeking hotels from hotel-base.com

@author: ytan
'''

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.selector import HtmlXPathSelector

from scrapers.common.items import BizItem
from scrapers.common import utils

class HotelBaseScraper(CrawlSpider):
    """ Crawl through web sites you specify """

    name = "hotelbase_scraper"

    start_urls,_ = utils.obtainURLsFromText()
    allowed_domains = ["hotel-base.com"]

    # Add our callback which will be called for every found link
    rules = [
        Rule(SgmlLinkExtractor(allow=('\.html',)), follow=True, callback="searchHotels")
    ]

    def __init__(self, *a, **kw):
        super(HotelBaseScraper, self).__init__(*a, **kw)

    def searchHotels(self, response):
        """search hotels in hotel-base.com"""
        item = BizItem()
        hxs = HtmlXPathSelector(response)
        hotels = hxs.select("//table[@class='cTx fA11n']")
        for h in hotels:
            name = h.select("tr/td/a/u/text()").extract()
            if name:
                item['name'] = name[0]
                info = h.select('tr/td[@style="vertical-align:top;"]/text()').extract()
                item['url']   = "http:"+info[3].split(":")[2]
                item['phone'] = info[2].split(":")[1]
                item['address']  = info[0]
                yield item

    def _requests_to_follow(self, response):

        if getattr(response, "encoding", None) != None:
            # Server does not set encoding for binary files
            # Do not try to follow links in
            # binary data, as this will break Scrapy
            return CrawlSpider._requests_to_follow(self, response)
        else:
            return []
