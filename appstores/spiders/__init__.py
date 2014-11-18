# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import urlparse

import scrapy
from scrapy.utils.project import get_project_settings


class XSpider(scrapy.Spider):
    _url_format = ''

    def __init__(self, *args, **kwargs):
        super(XSpider, self).__init__(*args, **kwargs)
        self.start_urls = []

        settings = get_project_settings()
        for kw in settings.get('SEARCH_KEYWORDS'):
            self.start_urls.append(self._url_format % kw)

        self.ranking_dict = {}

    def _get_search_keyword_from_q(self, key, url):
        qs = urlparse.urlparse(url).query
        k = urlparse.parse_qs(qs).get(key)[0]
        k = k.decode('utf8')
        return k

    def parse_specified_item(self, response):
        raise NotImplemented

    def _populate_ranking(self, response):
        raise NotImplemented
