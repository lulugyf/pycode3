# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Money163Pipeline(object):
    def process_item__(self, item, spider):
        url = item['news_url']
        print("----url:", url)
        filename = url.split("/")[-1].split(".")[0]
        fo = open(filename, "w", encoding="UTF-8")
        fo.write(str(dict(item)))
        fo.close()
        return None # item

    def process_item(self, item, spider):
        return item
