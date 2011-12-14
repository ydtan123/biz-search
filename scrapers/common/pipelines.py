# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from dbs.dbapi import Business, Email, open_db, close_db

class BasePipeline(object):
    def __init__(self):
        print "++++++++ In base pipeline"
        self.conn = open_db("bizsearch_work")
        self.dbcursor = self.conn.cursor()

    def __del__(self):
        self.dbcursor.close()
        close_db(self.conn)

    def process_item(self, **kwargs):
        self.table.insert_one_by_names(self.dbcursor, **kwargs)
        self.table.commit(self.dbcursor)


class BizPipeline(BasePipeline):
    def __init__(self):
        print "+++++++++ bizpipeline"
        super(BizPipeline, self).__init__()
        self.table = Business

    def process_item(self, item, spider):
        print "++++", item
        super(BizPipeline, self).process_item(
                            name=item['name'],
                            url=item['url'],
                            phone=item['phone'],
                            address=item['address'],
                            category='TUR'
                            )
        return item

class EmailPipeline(BasePipeline):
    def __init__(self):
        self.table = Email

    def process_item(self, item, spider):
        print "++++", item
        super(EmailPipeline, self).process_item(
                            address=item['address'],
                            biz_id=item['biz_id'],
                            )
        return item
