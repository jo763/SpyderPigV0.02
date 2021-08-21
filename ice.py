# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:07:41 2019

@author: PROL1661
"""

import scrapy

from fielditem import FieldItem

class IceSpider(scrapy.Spider):
    # Name of spider that will be ran
    name = 'ice'
    # The websites URLs also contain the specific target location, in this case London + 20 miles
    # The event page urls, really there should be a script checking if more pages pages, but it's so far in the future that it doesn't matter. If page 4 doesn't exist etc. doesn't matter)
    base_url = 'https://www.ice.org.uk/events?_=1568793275588&distance=20&page='
    start_urls = []
    for i in range(1,17):
        i = str(i)
        url = base_url + i
        start_urls.append(url)
#    start_urls = ['https://www.ice.org.uk/events?_=1568793275588&distance=20',
#                  'https://www.ice.org.uk/events?location=London%2C%20UK&distance=20&latitude=51.5073509&longitude=-0.12775829999998223&_=1568793275589&page=2',
#                  'https://www.ice.org.uk/events?location=London%2C%20UK&distance=20&latitude=51.5073509&longitude=-0.12775829999998223&_=1568793275589&page=3'
#                ]
    

    # This function essentially finds all the events on the page and then gets the spider to scrape those event pages.
    def parse(self, response):
            
            base_url = 'https://www.ice.org.uk'

            # Scrapes all the weblinks to the individual events
            all_links = response.css('div.event-info')
            
            # For every link in all_links, follow the url and scrape the page
            for link in all_links:
                webLink = link.css('a::attr(href)').get()
                # Creates the full url. e.g. bbc.co.uk + /news = bbc.co.uk/news
                absolute_url = base_url + webLink
                # Follows the url, activates the parse_attr function for that page.
                yield scrapy.Request(absolute_url, callback = self.parse_attr)
               
    # This function scrapes all the relevant data from the event page, incl cost, title, description, date, location          
    def parse_attr(self, response):
        
        # Standard extraction of data using css selectors
        eventName = response.css('h1::text').extract()
        eventDetails = response.css('div.icn-list')
        eventLocation = eventDetails.css('li.icn-pin::text').extract()
        eventDate = response.css('li.icn-date::text').extract()
        
        # Need to do sub extractions so have some intermediate, I'm sure there's a better way than this, but it works
        eventCostInfo = response.css('div.hero-content')
        eventCost = eventCostInfo.css('h3::text').extract()        
        #eventDescInfo = response.css('div.grid12')
        #eventDescription = eventDescInfo.css('p::text').extract_first()
        
        # Tries to convert the dates into real dates
        if len(eventDate) >0:
            eventDate = eventDate[0].strip()

        eventInstitution = 'ICE'
        
        items = FieldItem()
       
        items["eventCost"] = eventCost
        items["eventLocation"] = eventLocation
        items["eventDate"] = eventDate
        items['eventLink'] = response.request.url
        items['eventInstitution'] = eventInstitution
        items["eventName"] = eventName
        #items['eventDescription'] = eventDescription
        yield items