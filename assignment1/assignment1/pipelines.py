# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class Assignment1Pipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
        "localhost",
        27017)
        db = connection["assignment1"]
        self.collection1 = db["expat_topics"]
        self.collection2 = db["expat_posts"]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            if 'author' in dict(item).keys():
                self.collection2.insert_one(dict(item))
            else:
                self.collection1.insert_one(dict(item))
        return item





# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html





