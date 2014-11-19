#!-*- coding: utf8 -*-

import re

import requests
import scrapy

from appstores.items import AppstoresItem
from appstores.spiders import XSpider


_id_reg = re.compile(r'/detail/index/soft_id/(\d+)\?')
_pkname_reg = re.compile(r'\'pname\':\s*\'(.*?)\'')
_baike_cmc_reg = re.compile(r'\'baike_name\':\s*\'(.*?)\'') # get comments count from baike
_msg_count_reg = re.compile(r'mesg":(\d+),')

_baike_url_format = ('http://intf.baike.360.cn/index.php?'
    'callback=jQuery17206597192140761763_1416375156832'
    '&name=%s&c=message&a=getmessagenum'
)


class QihooSpider(XSpider):
    name = "qihoo"

    allowed_domains = ["zhushou.360.cn",]

    _url_format = 'http://zhushou.360.cn/search/index/?kw=%s'

    def parse_specified_item(self, response):
        display_name = response.css('#app-name span::text').extract()[0]

        package_name = _pkname_reg.search(response.body).groups()[0]

        url = response.request.url
        pk = _id_reg.search(url).groups()[0]
        ranking = self.ranking_dict[pk]

        keyword = self._get_search_keyword_from_q('recrefer', url)
        keyword = keyword.split('_')[2]

        dlcount = response.xpath(
            '//span[@class="s-3"][position()=1]/text()'
        ).extract()[0]
        dlcount = dlcount.split(u'：')[1]

        baike_txt = _baike_cmc_reg.search(response.body).groups()[0]
        req = requests.get(_baike_url_format % baike_txt)
        comment_count = _msg_count_reg.search(req.content).groups()[0]

        tag_box = response.css('.app-tags a::text').extract()
        category = '##'.join(tag_box)

        update_time = response.css(
            'div.base-info table td::text'
        ).extract()[1]

        version = response.css(
            'div.base-info table td::text'
        ).extract()[2]

        rating = response.css('span.s-1::text').extract()[0]
        rating = int(float(rating) * 10)

        item = AppstoresItem(package_name=package_name,
            display_name=display_name, keyword=keyword, dlcount=dlcount,
            comment_count=comment_count, category=category, rating=rating,
            update_time=update_time, version=version, ranking=ranking,
        )
        yield item

    def _populate_ranking(self, response):
        lis = response.css('dd h3 a')
        ranking = 1
        for li in lis:
            pk = li.xpath('@href').extract()[0]
            result = _id_reg.search(pk)
            pk = result.groups()[0]
            self.ranking_dict[pk] = ranking
            ranking += 1

    def parse(self, response):
        self._populate_ranking(response)

        links = response.css('dd h3 a')
        for link in links:
            prefix = 'http://zhushou.360.cn'
            url = link.xpath('@href').extract()[0]
            url = prefix + url
            yield scrapy.Request(url, callback=self.parse_specified_item)
