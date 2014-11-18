# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoresItem(scrapy.Item):
    # define the fields for your item here like:
    display_name = scrapy.Field()
    package_name = scrapy.Field()
    keyword = scrapy.Field()
    dlcount = scrapy.Field()
    comment_count = scrapy.Field()
    category = scrapy.Field()
    update_time = scrapy.Field()
    version = scrapy.Field()
    ranking = scrapy.Field()
    rating = scrapy.Field()
