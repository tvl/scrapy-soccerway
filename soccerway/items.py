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

class Venue(Item):
    id = Field()
    name = Field()
    country = Field()
    founded = Field()
    address = Field()
    zip = Field()
    city = Field()
    opened = Field()
    capacity = Field()
    surface = Field()
    previous_names = Field()
    facts = Field()

class Team(Item):
    id = Field()
    name = Field()
    area_id = Field()
    area_name = Field()
    country = Field()
    founded = Field()
    address = Field()
    phone = Field()
    fax = Field()
    email = Field()
    website = Field()

class Match(Item):
    id = Field()
    datetime = Field()
    area_id = Field()
    area_name = Field()
    competition_id = Field()
    competition_name = Field()
    home_team_id = Field()
    home_team = Field()
    away_team_id = Field()
    away_team = Field()
    kick_off = Field()
    score = Field()
    updated = Field()

class Area(Item):
    id = Field()
    name = Field()
    updated = Field()

class Competition(Item):
    id = Field()
    name = Field()
    area_id = Field()
    area_name = Field()
    updated = Field()


