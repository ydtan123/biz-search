# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BizItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url = Field()
    name = Field()
    phone = Field()
    address = Field()

    def __str__(self):
        return "BizURL: name=%s url=%s phone=%s" % (self['name'], self['url'], self['phone'])

