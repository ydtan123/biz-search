# Scrapy settings for myscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'hotelbase_scraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['hotelbase_scraper.spiders']
NEWSPIDER_MODULE = 'hotelbase_scraper.spiders'
DEFAULT_ITEM_CLASS = 'hotelbase_scraper.items.BizItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [ 'hotelbase_scraper.pipelines.HotelBaseScraperPipeline' ]

DEPTH_LIMIT = 3



