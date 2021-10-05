# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class NetEmpregosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    job_description = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    post_date = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    scrape_date = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    company = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    job_location = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    job_category = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())
    job_href = scrapy.Field(input_processor=MapCompose(remove_tags),
                             output_processor=TakeFirst())

def clear_spaces(string):
    return string.strip()

class BonsEmpregosItem(scrapy.Item):

    job_title = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_description = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    post_date = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    scrape_date = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    company = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_location = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_category = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_href = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())


class EmpregoXlItem(scrapy.Item):

    job_title = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_description = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    post_date = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    scrape_date = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    company = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_location = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_category = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())
    job_href = scrapy.Field(input_processor=MapCompose(remove_tags, clear_spaces),
                             output_processor=TakeFirst())