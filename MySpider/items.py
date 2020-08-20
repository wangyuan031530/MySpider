# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *

db = MySQLDatabase('wangyuan', host='49.233.128.194', port=3306, user='root', passwd='Yuan031530', charset='utf8')


class ZycgItem(scrapy.Item):
    company = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    mobile = scrapy.Field()


class Phonenums(Model):
    company = CharField(verbose_name="company", max_length=100, null=False)
    name = CharField(verbose_name="name", max_length=200, null=False)
    address = CharField(verbose_name="address", max_length=80, null=False)
    phone = CharField(verbose_name="phone", max_length=100, null=False)
    mobile = CharField(verbose_name="mobile", max_length=100, null=False)

    class Meta:
        database = db
