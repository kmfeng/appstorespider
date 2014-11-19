# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

from .settings import (DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWD, DB_TABLE)


_db = MySQLdb.connect(
    host=DB_HOST, db=DB_NAME, port=DB_PORT,
    user=DB_USER, passwd=DB_PASSWD, use_unicode=True,
)
_db.set_character_set('utf8')


class AppstoresPipeline(object):
    _sql_format = (
        u'INSERT INTO {table}('
        'display_name, package_name, keyword, dlcount,'
        'comment_count, category, update_time, version,'
        'ranking, rating) VALUES("{{display_name}}", "{{package_name}}",'
        '"{{keyword}}", "{{dlcount}}", "{{comment_count}}", "{{category}}",'
        '"{{update_time}}", "{{version}}", {{ranking}}, {{rating}})'
    ).format(table=DB_TABLE)

    def _insert_into_db(self, item):
        # TODO: security check, exception process, etc.
        sql = self._sql_format.format(**item)
        cursor = _db.cursor()
        cursor.execute(sql)
        _db.commit()

    def process_item(self, item, spider):
        self._insert_into_db(item)
        return item
