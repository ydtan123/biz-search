# Scrapy settings for myscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'hotelbase_scraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['hotelbase_scraper']
NEWSPIDER_MODULE = 'hotelbase_scraper'
DEFAULT_ITEM_CLASS = 'hotelbase_scraper.items.BizItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [ 'scrapers.common.pipelines.BizPipeline' ]

DEPTH_LIMIT = 1



