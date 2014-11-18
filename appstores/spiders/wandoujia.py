#!-*- coding: utf8 -*-

import urlparse

import scrapy
from scrapy.utils.project import get_project_settings

from appstores.items import AppstoresItem


class WandoujiaSpider(scrapy.Spider):
    name = "wandoujia"

    allowed_domains = ["www.wandoujia.com",]

    _url_format = 'http://www.wandoujia.com/search?key=%s&source=appcategory'

    def __init__(self, *args, **kwargs):
        super(WandoujiaSpider, self).__init__(*args, **kwargs)
        self.start_urls = []

        settings = get_project_settings()
        for kw in settings.get('SEARCH_KEYWORDS'):
            self.start_urls.append(self._url_format % kw)

        self.ranking_dict = {}

    def _get_search_keyword_from_q_key(self, url):
        qs = urlparse.urlparse(url).query
        k = urlparse.parse_qs(qs).get('key')[0]
        k = k.decode('utf8')
        return k

    def parse_specified_item(self, response):
        display_name = response.css(
            '.app-name span.title').xpath('text()'
        ).extract()[0]

        package_name = response.request.url.split('apps/')[1]

        ranking = self.ranking_dict[package_name]

        refer = response.request.headers.get('Referer')
        keyword = self._get_search_keyword_from_q_key(refer)

        num_list = response.css('.num-list')
        dlcount = num_list.xpath(
            '//span/i[@itemprop="interactionCount"]/text()'
        ).extract()[0]

        comment_count = response.xpath(
            '//a[@href="#comments"]/i/text()'
        ).extract()[0]

        tag_box = response.xpath(
            '//a[@itemprop="SoftwareApplicationCategory"]/text()'
        ).extract()
        category = '##'.join(tag_box)

        update_time = response.xpath(
            '//time[@itemprop="datePublished"]/@datetime'
        ).extract()[0]

        version = response.css('dl.infos-list').xpath(
            '//dd[4]/text()'
        ).extract()[0]

        item = AppstoresItem(package_name=package_name,
            display_name=display_name, keyword=keyword, dlcount=dlcount,
            comment_count=comment_count, category=category,
            update_time=update_time, version=version, ranking=ranking,
        )
        yield item

    def _populate_ranking(self, response):
        lis = response.css('li.card')
        ranking = 1
        for li in lis:
            pk = li.xpath('@data-pn').extract()[0]
            self.ranking_dict[pk] = ranking
            ranking += 1

    def parse(self, response):
        self._populate_ranking(response)

        links = response.css('a.name')
        for link in links:
            url = link.xpath('@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_specified_item)
