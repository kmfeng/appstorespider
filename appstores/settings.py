# -*- coding: utf-8 -*-

# Scrapy settings for appstores project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'appstores'

SPIDER_MODULES = ['appstores.spiders']
NEWSPIDER_MODULE = 'appstores.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ('Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X;'
     'en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/'
     '8H7 Safari/6533.18.5')

SEARCH_KEYWORDS = [
    u'浏览器', u'手机浏览器', u'网页浏览器',
    u'网页', u'欧朋', u'欧朋浏览器',
]
