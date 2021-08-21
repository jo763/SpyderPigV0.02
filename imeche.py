# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:09:45 2019

@author: PROL1661
"""


import scrapy

from fielditem import FieldItem

class ImecheSpider(scrapy.Spider):
    name = 'imeche'
    
    start_urls = ['http://nearyou.imeche.org/near-you/UK/Merseyside---North-Wales/Events',
                  'http://nearyou.imeche.org/near-you/UK/Northern-Ireland/events',
                  'http://nearyou.imeche.org/near-you/UK/South-Wales/events',
                  'http://nearyou.imeche.org/near-you/UK/Western/events'
                ]
    
    
    base_urls = ['http://nearyou.imeche.org/near-you/UK/Greater-London/events?p=', 'http://nearyou.imeche.org/near-you/UK/East-Midlands/events?p=', 
                 'http://nearyou.imeche.org/near-you/UK/Eastern/events?p=', 'http://nearyou.imeche.org/near-you/UK/Midland/events?p=',
                 'http://nearyou.imeche.org/near-you/UK/North-Eastern/events?p=', 'http://nearyou.imeche.org/near-you/UK/North-Western/events?p=',
                 'http://nearyou.imeche.org/near-you/UK/Scottish-Region/events?p=', 'http://nearyou.imeche.org/near-you/UK/South-Eastern/events?p=',
                 'http://nearyou.imeche.org/near-you/UK/Thameswey/about-us?p=', 'http://nearyou.imeche.org/near-you/UK/Wessex/events?p=',
                 'http://nearyou.imeche.org/near-you/UK/Yorkshire/events?p=']
    
    for url in base_urls:
        for i in range (1,7):
            i = str(i)
            url_to_add = url + i
            start_urls.append(url_to_add)
        
    
    
    
    

    def parse(self, response): # response contains the sourcecode of the site we want to scrape
        
        base_url = 'http://nearyou.imeche.org'
        
        all_links = response.css('li.event-item')
        
        for link in all_links:
            webLink = link.css('div.event-title a::attr(href)').get()
            absolute_url = base_url + webLink
            yield scrapy.Request(absolute_url, callback = self.parse_attr)

    
    def parse_attr(self, response):
        items = FieldItem()
        
        try:
            eventCost = response.css('td.price::text').extract()
        except:
            eventCost = 'Cannot Determine'
        if eventCost == None or len(eventCost) < 2:
            eventCost = 'Cannot Determine'
        
        
        eventCost = response.css('td.price::text').extract()

        items['eventCost'] = eventCost
        
        eventName = response.css('span.title::text').extract()
        items["eventName"] = eventName
        
        eventInstitution = 'IMechE'
        items['eventInstitution'] = eventInstitution
        
        items['eventLink'] = response.request.url
        
#        eventDesc = response.css('div.event-description')
#        for desc in eventDesc:
#            eventDescription = desc.css('p::text').extract()
#            items['eventDescription'] = eventDescription
        
        eventDetails = response.css('div.event-detail.section')
        for date in eventDetails:
            eventDate = date.css('span::text').extract()
            eventDate = eventDate[1]
            items["eventDate"] = eventDate
            
        addressDetails = response.css('div.event-address.section')
        for address in addressDetails:
            eventLocation = address.css('p::text').extract()
            items["eventLocation"] = eventLocation
            
        yield items