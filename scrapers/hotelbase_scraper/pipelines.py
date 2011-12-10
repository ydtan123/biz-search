# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from dbs import Business, open_db

class HotelBaseSpiderPipeline(object):
    def __init__():
        open_db("business")
 
    def process_item(self, item, spider):
        Business.insert_one(name=item['name'],
                            url=item['url'],
                            phone=item['phone']
                            )
        return item
