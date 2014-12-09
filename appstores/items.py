# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoresItem(scrapy.Item):
    '''
        item that will be stored in db, the mean of fields are:
        display_name:
            name displayed in pages, eg. '欧朋浏览器'

        package_name:
            apk's package name, eg. 'com.oupeng.browser'

        keyword:
            keywords used to search in market, it can be seen in
            `appstores.settings.SEARCH_KEYWORDS`

        dlcount: download count
        comemnt_count: comment count
        category: apk's category in targeted market
        update_time: apk's latest update time
        version: apk's version
        ranking: the order in search result
        rating: rating in targeted market
        store_name: targeted app store's name
    '''

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
    store_name = scrapy.Field()
