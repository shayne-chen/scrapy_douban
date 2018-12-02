# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class DoubanPipeline(object):
	def __init__(self):
		host = settings["MONGODB_HOST"]
		port = settings["MONGODB_PORT"]
		dbname = settings["MONGODB_DBNAME"]

		client = pymongo.MongoClient(host=host, port=port)
		db = client[dbname]
		self.collection = db[settings["MONGODB_TABLE"]]

	def process_item(self, item, spider):
		person_comment = dict(item)
		self.collection.insert(person_comment)
		return item
        
