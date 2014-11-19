#!-*- coding: utf8 -*-

import re
import urlparse

import scrapy

from appstores.items import AppstoresItem
from appstores.spiders import XSpider


class WandoujiaSpider(XSpider):
    name = "91"

    allowed_domains = ["market.91.com",]

    _url_format = 'http://market.91.com/Android/1/Search/%s'

    def parse_specified_item(self, response):
        display_name = response.css('div.fl_wrap').xpath(
            '//dt/a/text()'
        ).extract()[0]

        package_name = response.xpath('//div[@id="identifier"]/text()').extract()[0]

        ranking = int(response.request.url.split('/')[-1].split('?')[0]) - 240100

        url = response.request.url
        keyword = self._get_search_keyword_from_q('kw', url)

        content = response.css('div.soft_info::text').extract()
        category = content[0].split(u'：')[1]

        version = content[1].split(u'：')[1]

        dlcount = content[4].split(u'：')[1]

        rating = None
        rating_percent = response.xpath(
            '//span[@class="star_on"]/@style'
        ).extract()[0]
        pattern = re.compile(r'width:(\d+)%')
        result = pattern.search(rating_percent)
        if result:
            rating = int(result.groups()[0])

        comment_count = None

        update_time = None

        item = AppstoresItem(package_name=package_name,
            display_name=display_name, keyword=keyword, dlcount=dlcount,
            comment_count=comment_count, category=category, rating=rating,
            update_time=update_time, version=version, ranking=ranking,
        )
        yield item

    def parse(self, response):
        kw = response.request.url.split('/')[-1]

        links = response.css('dl.app_col')
        for link in links:
            prefix = 'http://market.91.com'
            url = link.xpath('@accesskey').extract()[0]
            url = prefix + url + '?kw=%s' % kw
            yield scrapy.Request(url, callback=self.parse_specified_item)
