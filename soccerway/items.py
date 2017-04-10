# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class SoccerwayItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Match(Item):
    home = Field()
    away = Field()

class Area(Item):
    ID = Field()
    name = Field()
    updated = Field()

class Competition():
    ID = Field()
    name = Field()
    area_id = Field()
    area_name = Field()
    updated = Field()


