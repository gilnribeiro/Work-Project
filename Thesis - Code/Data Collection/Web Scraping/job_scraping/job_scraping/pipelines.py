# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json


class JobScrapingPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class TooManyEmptyFields:
    """
    Drop Job vacancies that have:
    job_title or job_description = ''
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('job_title') != '' and adapter.get('job_description') != '':
            return item
        else:
            raise DropItem(f"Missing Job title or job_description in {item}")


class DuplicatesPipeline:
    """
    Drop duplicate job urls directly from scraping 
    (cover the possibility of a job being posted twice in the same page)
    """

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['job_href'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['job_href'])
            return item

