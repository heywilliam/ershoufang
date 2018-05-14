# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ErshoufangItem(Item):

    title = Field()
    block = Field()
    layout = Field()
    area = Field()
    direction = Field()
    decoration = Field()
    elevator = Field() #部分有
    floor = Field()
    age = Field()
    location = Field()
    followers = Field()
    posttime = Field()
    totalprice = Field()
    unitprice = Field()
    detailpage = Field()
    subway = Field() #部分有
    taxfree = Field() #部分有
    district =Field()



