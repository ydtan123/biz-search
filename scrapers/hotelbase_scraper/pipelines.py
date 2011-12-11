# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from dbs.dbapi import Business, open_db

class HotelBaseScraperPipeline(object):
    def __init__(self):
        self.conn = open_db("bizsearch")
        self.dbcursor = self.conn.cursor()

    def __del__(self):
        self.dbcursor.close()
        close_db(self.conn)

    def process_item(self, item, spider):
        print "++++", item
        Business.insert_one_by_names(
                            self.dbcursor,
                            name=str(item['name']).strip(),
                            url=str(item['url']).strip(),
                            phone=str(item['phone']).strip(),
                            address=str(item['address']).strip(),
                            category='TUR'
                            )
        Business.commit(self.dbcursor)
        return item
