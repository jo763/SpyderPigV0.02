# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:10:42 2019

@author: PROL1661
"""
import scrapy

from fielditem import FieldItem

class EventbriteSpider(scrapy.Spider):
    name = 'eventbrite'
    
    start_urls = ['https://www.eventbrite.co.uk/o/institution-of-structural-engineers-10903334794#']
                         #'https://www.eventbrite.co.uk/o/south-west-nuclear-hub-15158410273',
                         #'https://www.eventbrite.co.uk/o/the-institution-of-mechanical-engineers-14145688499',
                         #'https://www.eventbrite.com/o/ice-london-gamps-18020286147'
                #]
    
       
    
    def parse(self, response): # response contains the sourcecode of the site we want to scrape
        
        
        items = FieldItem()
        
        
        eventData = response.css('div.list-card__body') # Gets division tags with classes of quote
        all_headers = response.css('div.list-card__header')
        
        for eventDetail in eventData:
             
            eventName = eventDetail.css('div.list-card__title::text').extract()
            eventDate = eventDetail.css('time.list-card__date::text').extract()
            eventLocation = eventDetail.css('div.list-card__venue::text').extract()
            #eventDescription = quotes.css('NOT ENTERED::text').extract()
            
            
            items["eventName"] = eventName
            items["eventDate"] = eventDate
            items["eventLocation"] = eventLocation
            #items['eventDescription'] = eventDescription    
            items['eventInstitution'] = 'IstructE'
            yield items
        
        for header in all_headers:
            eventCost = header.css('span.list-card__label::text').extract()
            #if not eventCost[0]:
                #items["eventCost"] = "Unknown (sold out?)"
            #else:
               
            items["eventCost"] = eventCost
        yield items