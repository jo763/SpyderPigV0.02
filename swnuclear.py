# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:16:59 2019

@author: PROL1661
"""

import scrapy

from fielditem import FieldItem

class SWNuclearHubEventbriteSpider(scrapy.Spider):
    name = 'SWNuclearHub'
    
    start_urls = ['https://www.eventbrite.co.uk/o/south-west-nuclear-hub-15158410273']

    
       
    
    def parse(self, response): # response contains the sourcecode of the site we want to scrape
        
        
        items = FieldItem()
        
        
        eventData = response.css('div.list-card__body') # Gets division tags with classes of quote
        all_headers = response.css('div.list-card__header')
        
        for eventDetail in eventData:
             
            eventName = eventDetail.css('div.list-card__title::text').extract()
            eventDate = eventDetail.css('time.list-card__date::text').extract()
            eventLocation = eventDetail.css('div.list-card__venue::text').extract()
            #eventLink = quotes.css('NOT ENTERED::text').extract()
            
            
            items["eventName"] = eventName
            items["eventDate"] = eventDate
            items["eventLocation"] = eventLocation
            items['eventLink'] = eventLink    
            #items['eventInstitution'] = 'SW Nuclear'
            yield items
        
        for header in all_headers:
            eventCost = header.css('span.list-card__label::text').extract()
            #if not eventCost[0]:
                #items["eventCost"] = "Unknown (sold out?)"
            #else:
               
            items["eventCost"] = eventCost
        yield items