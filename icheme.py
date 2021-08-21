# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:00:31 2019

@author: PROL1661
"""

import scrapy
from fielditem import FieldItem

class IchemeSpider(scrapy.Spider):
    # Name of spider that will be ran
    name = 'icheme' 
    
    # The event page urls, really there should be a script checking if more pages pages, but it's so far in the future that it doesn't matter. If therepage 4 doesn't exist etc. doesn't matter)
    start_urls = ['https://www.icheme.org/membership/communities/all-upcoming-events/page-1/',
                  'https://www.icheme.org/membership/communities/all-upcoming-events/page-2/',
                  'https://www.icheme.org/membership/communities/all-upcoming-events/page-3/',
                  'https://www.icheme.org/membership/communities/all-upcoming-events/page-4/'
                ]
    
    # This function essentially finds all the events on the page and then gets the spider to scrape those event pages.
    def parse(self, response): 
            base_url = 'https://www.icheme.org'
            # Scrapes all the weblinks to the individual events
            all_links = response.css('a.event-list-panel.event-list-panel--has-img::attr(href)')
            # For every link in all_links, follow the url and scrape the page.
            for link in all_links:
                # Gets the weblink
                webLink = link.get()
                # Creates the full url. e.g. bbc.co.uk + /news = bbc.co.uk/news
                absolute_url = base_url + webLink
                # Follows the url, activates the parse_attr function for that page.
                yield scrapy.Request(absolute_url, callback = self.parse_attr)

    # This function scrapes all the relevant data from the event page, incl cost, title, description, date, location
    def parse_attr(self, response):
        # Fields the item
        items = FieldItem()
        # Name of this instituation
        eventInstitution = 'IChemE'
        # Extracting the name of the event
        eventName = response.css('h1.section-title::text').extract()
        # Most of the details are in this box. so will subscrape from it.
        eventDetails = response.css('li.event-overview__item')
        # This is a fun part where most of these html tags have the same name and some may not exist. So we extract their titles and info into lists and start filtering them.
        eventInfo = eventDetails.css('span.event-overview__val::text').extract()
        eventTitle = eventDetails.css('span.event-overview__label::text').extract()

        # If there is a price given, it extracts the price, otherwise says unknown    
        if 'Price' in eventTitle:
            eventTitleIndex = eventTitle.index('Price')
            eventCost = eventInfo[eventTitleIndex]
        else:
            eventCost = 'Unknown'
        
        # If there is a date given, it extracts the date, otherwise says unknown.
        # This has been placed under different tags of 'Date From' and 'Dates' so need to check both.
        if 'Date From' in eventTitle or 'Dates' in eventTitle:
            if 'Date From' in eventTitle:
                eventTitleIndex = eventTitle.index('Date From')
            else:
                eventTitleIndex = eventTitle.index('Dates') 
            eventDate = eventInfo[eventTitleIndex]
        else:
            eventDate = 'Unknown'
            
        # If there is a location given, it extracts the location, otherwise says unknown    
        if 'Location' in eventTitle:
            eventTitleIndex = eventTitle.index('Location')
            eventLocation = eventInfo[eventTitleIndex]
        else:
            eventLocation = 'Unknown'
        
        # Extracts the whole description, but it's noted that it's stupidly long, so the first paragraph of it is scraped and the rest scrapped.
        #paragraphInfo = response.css('div.umb-body.umb-body--m-bottom')
        #eventDescription = paragraphInfo.css('p::text').extract_first()

        # Filters out all the events that are not in London. An improvement would be to check all post codes in London.
        if 'London' in eventLocation or 'SW' in eventLocation or 'Online' in eventLocation or 'NW' in eventLocation or 'SE' in eventLocation or 'Surrey':
            items["eventCost"] = eventCost
            items["eventLocation"] = eventLocation
            items["eventDate"] = eventDate
            items['eventLink'] = response.request.url
            items['eventInstitution'] = eventInstitution
            items["eventName"] = eventName
            #items['eventDescription'] = eventDescription
            yield items