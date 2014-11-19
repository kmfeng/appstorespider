#!-*- coding: utf8 -*-

import re

import scrapy

from appstores.items import AppstoresItem
from appstores.spiders import XSpider


class BaiduSpider(XSpider):
    name = "baidu"

    allowed_domains = ["shouji.baidu.com",]

    _url_format = 'http://shouji.baidu.com/s?wd=%s&data_type=app&from=landing'

    def parse_specified_item(self, response):
        display_name = response.css(
            'div.app-intro h1.app-name span'
        ).xpath('text()').extract()[0]

        package_name = response.xpath(
            '//div[@class="area-download"]/a[position()=1]/@data_package'
        ).extract()[0]

        ranking = self.ranking_dict[package_name]

        keyword = ''
        url = response.request.url
        _keyword = self._get_search_keyword_from_q('f', url)
        pattern = re.compile(r'search_app_(.*?)@')
        result = pattern.search(_keyword)
        if result:
            keyword = result.groups()[0]

        num_list = response.css('span.download-num::text').extract()[0]
        dlcount = num_list.split(':')[1].strip()

        comment_count = ''

        category = response.xpath(
            '//div[@class="nav"]/span[position()=3]/a/text()'
        ).extract()[0]

        update_time = ''

        version = response.css('span.version::text').extract()[0]
        version = version.split(':')[1].strip()

        # NOTE: 评分为100分制
        rating = ''
        rating_percent = response.css('span.star-percent').xpath('@style').extract()[0]
        pattern = re.compile(r'width:(\d+)%')
        result = pattern.search(rating_percent)
        if result:
            rating = int(result.groups()[0])

        item = AppstoresItem(package_name=package_name,
            display_name=display_name, keyword=keyword, dlcount=dlcount,
            comment_count=comment_count, category=category, rating=rating,
            update_time=update_time, version=version, ranking=ranking,
        )
        yield item

    def _populate_ranking(self, response):
        apps = response.css('div.app div.little-install a')
        ranking = 1
        for app in apps:
            pk = app.xpath('@data_package').extract()[0]
            self.ranking_dict[pk] = ranking
            ranking += 1

    def parse(self, response):
        self._populate_ranking(response)

        links = response.css('div.app div.top a')
        prefix = 'http://shouji.baidu.com'
        for link in links:
            url = link.xpath('@href').extract()[0]
            url = prefix + url
            yield scrapy.Request(url, callback=self.parse_specified_item)
