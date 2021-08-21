# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:08:42 2019

@author: PROL1661
"""

import scrapy
from fielditem import FieldItem

class IopSpider (scrapy.Spider):
    # Name of spider that will be ran
    name = 'iop'
       
    # The event page urls, really there should be a script checking if more pages pages, but it's so far in the future that it doesn't matter. If therepage 4 doesn't exist etc. doesn't matter)
    start_urls = ['https://events.iop.org/']
    def parse(self, response): 
        base_url = 'https://events.iop.org'
        # Scrapes all the weblinks to the individual events
        all_links = response.css('h5.card-title')
        # For every link in all_links, follow the url and scrape the page.
        for link in all_links:
            # Gets the weblink
            webLink = link.css('a::attr(href)').get()
            #webLink = link.get()
            # Creates the full url. e.g. bbc.co.uk + /news = bbc.co.uk/news
            absolute_url = base_url + webLink
            # Follows the url, activates the parse_attr function for that page.
            yield scrapy.Request(absolute_url, callback = self.parse_attr)
 

    def parse_attr(self, response):
        items = FieldItem()
        eventInstitution = "IoP"
        eventName = response.css("h1::text").extract()
        eventDetails = response.css("div.mb-3")
        #eventLocationDetails = response.css("div.col-lg-4")
        eventLocation = response.css("div.location__display::text").extract()
        eventDate = eventDetails.css("div::text").extract()
        
#        print("\n========================================================================\n")
#        print(eventDate)
#        print("\n========================================================================\n")
        
        
        
        items['eventInstitution'] = eventInstitution
        items["eventName"] = eventName
        items["eventDate"] = eventDate
        items["eventLocation"] = eventLocation
        items['eventLink'] = response.request.url
        
        
        yield items