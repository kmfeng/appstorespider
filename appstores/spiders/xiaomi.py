#!-*- coding: utf8 -*-

import re
import json

import requests
import scrapy

from appstores.items import AppstoresItem
from appstores.spiders import XSpider


_id_reg = re.compile(r'&id=(\d+)#page=detail')
_keywords_reg = re.compile(r'"zh_CN":\"(.*?)\"}')

_detail_api_format = 'http://m.app.mi.com/detailapi/%s'


class XiaomiSpider(XSpider):
    name = "xiaomi"

    allowed_domains = ["app.mi.com",]

    _url_format = 'http://m.app.mi.com/searchapi?keywords=%s&pageIndex=0&pageSize=20'

    def parse_specified_item(self, response):
        url = response.request.url

        id = _id_reg.search(url).groups()[0]
        result = requests.get(_detail_api_format % id)
        json_obj = json.loads(result.content)

        data = json_obj['appMap']
        display_name = data['displayName']

        package_name = ''

        ranking = self.ranking_dict[int(id)]

        keyword = self._get_search_keyword_from_q('word', url)

        category = _keywords_reg.search(data['keywords']).groups()[0]
        category = '##'.join(category.split(';'))

        keys = ['Rating1', 'Rating2', 'Rating3', 'Rating4', 'Rating5']
        comment_count = sum([int(data[k]) for k in keys])

        dlcount = ''

        update_time = data['uploadtime']

        version = data['vname']

        rating = int(float(data['appRater']) * 10)

        item = AppstoresItem(package_name=package_name,
            display_name=display_name, keyword=keyword, dlcount=dlcount,
            comment_count=comment_count, category=category, rating=rating,
            update_time=update_time, version=version, ranking=ranking,
        )
        yield item

    def parse(self, response):
        kw = self._get_search_keyword_from_q('keywords', response.request.url)
        url_format = 'http://m.app.mi.com/?word=%s&id=%s#page=detail'

        json_obj = json.loads(response.body)
        ranking = 1
        for d in json_obj['data']:
            pk = d['appId']
            self.ranking_dict[pk] = ranking
            ranking += 1

            url = url_format % (kw, pk)
            yield scrapy.Request(url, callback=self.parse_specified_item)
