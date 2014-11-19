#!-*- coding: utf8 -*-

import json
import datetime

import scrapy

from appstores.items import AppstoresItem
from appstores.spiders import XSpider


class YingyongbaoSpider(XSpider):
    name = "yingyongbao"

    allowed_domains = ["sj.qq.com",]

    _url_format = 'http://sj.qq.com/myapp/searchAjax.htm?kw=%s'

    def parse_specified_item(self, response):
        keyword = self._get_search_keyword_from_q('kw', response.request.url)

        json_obj = json.loads(response.body)
        ranking = 1
        for obj in json_obj['obj']['appDetails']:
            package_name = obj['pkgName']
            display_name = obj['appName']
            dlcount = obj['appDownCount']
            comment_count = ''
            category = obj['categoryName']

            update_time = datetime.datetime.fromtimestamp(obj['apkPublishTime'])
            update_time = update_time.strftime('%Y-%m-%d')

            version = obj['versionName']

            # 5分制 to 100分制
            rating = int(obj['averageRating'] * 20)

            item = AppstoresItem(package_name=package_name,
                display_name=display_name, keyword=keyword, dlcount=dlcount,
                comment_count=comment_count, category=category, rating=rating,
                update_time=update_time, version=version, ranking=ranking,
            )
            yield item
            ranking += 1

    def parse(self, response):
        return self.parse_specified_item(response)
