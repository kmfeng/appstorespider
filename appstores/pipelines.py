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
    def _insert_into_db(self, item):
        sql = 'INSERT INTO %s (%s) VALUES(%s);'
        keys = item.keys()
        values = item.values()

        fields = ','.join(keys)
        vcols_format = '%s,' * len(keys)
        vcols_format = vcols_format[:-1]

        sql = sql % (DB_TABLE, fields, vcols_format)

        cursor = _db.cursor()
        cursor.execute(sql, values)
        _db.commit()

    def process_item(self, item, spider):
        self._insert_into_db(item)
        return item
