# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:29:17 2019

@author: PROL1661
"""

import scrapy

class FieldItem(scrapy.Item):
    eventName = scrapy.Field()
    eventDate = scrapy.Field()
    eventLocation = scrapy.Field()
    eventCost = scrapy.Field()
    eventDescription = scrapy.Field()
    eventInstitution = scrapy.Field()
    eventLink = scrapy.Field()