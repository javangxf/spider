# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exceptions import DropItem

from spider.items import *


class SpiderPipeline(object):
    def __init__(self):
        self.movie = set()
        self.director = set()

    def open_spider(self, spider):
        self.file1 = open('films.json', 'w')
        self.file2 = open('director.json', 'w')

    def close_spider(self, spider):
        self.file1.close()
        self.file2.close()

    def process_item(self, item, spider):
        # print(item)
        name = item['name']
        # print(name)
        if isinstance(item, MoviesItem):
            if name in self.movie:
                raise DropItem("Duplicate book found:%s" % item)
            self.movie.add(name)
            line = json.dumps(dict(item)) + "\n"
            self.file1.write(line)
        else:
            if name in self.director:
                raise DropItem("Duplicate book found:%s" % item)
            self.movie.add(name)
            line = json.dumps(dict(item)) + "\n"
            self.file2.write(line)
        # print(line)
        return item
