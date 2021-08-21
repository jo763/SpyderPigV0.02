# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:58:26 2019

@author: PROL1661
"""

from scrapy.crawler import CrawlerProcess
import csv
from os import remove
import xlwings as xw
from easygui import *
# The below are spiders
from icheme import IchemeSpider
from ice import IceSpider
from imeche import ImecheSpider
from eventbrite import EventbriteSpider
from swnuclear import SWNuclearHubEventbriteSpider
from iop import IopSpider
  
# Results of the webscraping will go into an intemediate csv file.
csvFileName = 'CPD Events.csv'
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': csvFileName
})

# Activates the following webscraping spiders.
spiders = [IchemeSpider,IceSpider,ImecheSpider,EventbriteSpider,SWNuclearHubEventbriteSpider,IopSpider]
#spiders = [IopSpider]
#spiders = [ImecheSpider]
#spiders = [IchemeSpider]
for spider in spiders:
    process.crawl(spider)

# The script will stop here until the webcrawling is finished
process.start() 

# ===========================================================================================================================================================
# Rearranging the cells and generally organising the scraped data.

# ===========================================================================================================================================================

print("\n\nWebscraping finished, currently loading into excel file\n")

# Replaces any empty cells with 'Unknown'
def noBlanks(x):
    if x != '':
        pass
    else:
        x = 'Unknown'
    return x

def noBlanksCost(x):
    if x != '':
        pass
    else:
        x = 'Free (Potentially)'
    return x

def cleanUp (x):
    x = x.replace('\n',' ')
    x = x.replace('Online Webinar', 'Online')
    x = x.replace(',',' ')
    for i in range (10):
        x = x.replace('  ',' ')
    return x

def dateSuffixRemoval(x):
    x = x.replace('st','')
    x = x.replace('nd','')
    x = x.replace('rd','')
    x = x.replace('th','')
    x = x.replace('Augu','August')
    return x

def removeTime(x):
    if ':' in x:
        x = (x[:(x.index(':')-3)])
        #print(x)
        return x
    else:
        return x
    
def costCleanUp(x):
    x = x.replace('Free of charge and open to all','Free')
    x = x.replace('Free open to all','Free')
    x = x.replace('Free and open to all', 'Free')
    x = x.replace('Free of charge','Free')
    x = x.replace('Free of Charge','Free')
    x = x.replace('Free entry','Free')
    x = x.replace('FREE','Free')
    x = x.replace('free','Free')
    x = x.replace('£0.00','Free')
    #x = x.replace('0.00','Free')
    return x

#def formatDate(x):
#    try:
#        x = x.strftime('%d %b %Y')
#    except:
#        pass
   
eventNameList = []
eventDescList = []
eventDateList = []
eventCostList = []
eventInstList = []
eventLocationList = []
eventLinkList =[]

# Opens and reads the csv file using encoding utf8 
with open(csvFileName, 'r', encoding="utf8") as csvFile:
    reader = csv.reader(csvFile)
    # Skips the first line
    next(reader, None)
    
    # Strips the data found, getting rid of the random new lines and spaces from the cells in the csv file. Extracts and proceeds to add them to their respective lists
    for line in reader:
        eventNameList.append(noBlanks(cleanUp(line[6].strip())))
        #eventDescList.append(noBlanks(line[2].strip()))
        eventDateList.append(noBlanks(cleanUp(line[1].strip())))
        eventCostList.append(noBlanksCost(cleanUp(line[0].strip())))
        eventInstList.append(noBlanks(line[3].strip()))
        eventLocationList.append(noBlanks(cleanUp(line[5].strip())))
        eventLinkList.append(noBlanks(cleanUp(line[4].strip())))   

# Deletes the intermediate file
remove(csvFileName)

wb = xw.Book("CPD Events Tracker Template.xlsm")
iceSht = wb.sheets['ICE']
imecheSht = wb.sheets['IMechE']
ichemeSht = wb.sheets['IChemE']
iopSht = wb.sheets['IoP']
ietSht = wb.sheets['IET']
istructeSht = wb.sheets['IStructE']
#swNuclearSht = wb.sheets['SW Nuclear']

def exInput(sheetInput, rowInput):
    try:
        if eventNameList[event] == eventNameList[event - 1]:
            
            pass
    except:
        pass
        
    sheetInput.cells(rowInput, 1).value = eventNameList[event]
    sheetInput.cells(rowInput, 2).value = eventLocationList[event]
    sheetInput.cells(rowInput, 3).value = costCleanUp(eventCostList[event])
    sheetInput.cells(rowInput, 4).value = removeTime(dateSuffixRemoval(eventDateList[event]))
    sheetInput.cells(rowInput, 6).value = eventLinkList[event]

startRowInput = 8
ichemeRowInput = startRowInput
iceRowInput = startRowInput
imecheRowInput = startRowInput
iopRowInput = startRowInput
ietRowInput = startRowInput
istructeRowInput = startRowInput
swNuclearRowInput = startRowInput

shortMonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
cities = ['Aberdeen', 'Armagh', 'Bangor', 'Bath', 'Belfast', 'Birmingham', 'Bradford', 'Brighton', 'Bristol', 'Cambridge', 'Canterbury', 'Cardiff',
          'Carlisle', 'Chelmsford', 'Chester', 'Chichester', 'Coventry', 'Derby', 'Derry', 'Dundee', 'Durham', 'Edinburgh', 'Ely', 'Exeter', 
          'Glasgow', 'Gloucester', 'Herefird', 'Iverness', 'Hull', 'Lancaster', 'Leeds', 'Leicester', 'Lichfield', 'Lincoln', 'Lisburn',
          'London', 'Manchester', 'Newcastle', 'Newport', 'Newry', 'Norwucg', 'Nottingham', 'Oxford', 'Perth', 'Peterborough', 'Plymouth', 'Portsmouth',
          'Preston', 'Ripon', 'St Albans', 'St Asaph', 'St Davids', 'Salford', 'Salisbury', 'Sheffield', 'Southampton', ' Stirling', 'Stoke-on-Trent', 
          'Sunderland', 'Swansea', 'Truro', 'Wakefield', 'Wells', 'Westminster', 'Winchester', 'Wolverhampton', 'Worcester', 'York', 'Loughborough', 'Swindon',
          'Southend-on-Sea', 'Basildon', 'Norwich', 'Bedford', 'Hatfield', 'Yarmouth', 'Reading', 'Stafford', 'Telford', 'Hartlepool', 'Billingham', 'Warwick',
          'Hereford', 'Rugby', 'Barrow-in-Furness', 'Leamington Spa', 'Huddersfield', 'Rotherham', 'Poole', 'Pontefract', 'Halifax', 'Bournemouth', 'Brighouse',
          'Heath', 'Greenwich', 'Shoreham-by-Sea', 'Widnes', 'Workington', 'Dover', 'Thatcham', 'Adeversane', 'Arundel', 'Wigton', 'Amsterdam', 'Malaysia', 'Liverpool']

for event in range(len(eventInstList)):
    for city in cities:
        city_lower = city.lower()
        location_lower = eventLocationList[event].lower()
        if city_lower in location_lower:
            eventLocationList[event] = city
            break
    
#    if 'London' in eventLocationList[event]:
#        eventLocationList[event] = 'London'
    
    
    if eventInstList[event] == 'IChemE':
        tempCost = eventCostList[event].lower()
#        if "free" in tempCost:
#            eventCostList[event] = "Free"
        exInput(ichemeSht, ichemeRowInput)
        ichemeRowInput +=1
    elif eventInstList[event] == 'IET':
        exInput(ietSht, ietRowInput)
        ietRowInput +=1
    elif eventInstList[event] == 'IMechE':
#        if ':' in eventDateList[event]:
#            colonIndex = eventDateList[event].index(':')
#            eventDateList[event] = eventDateList[event][::colonIndex+1]
        exInput(imecheSht, imecheRowInput)
        imecheRowInput +=1
    elif eventInstList[event] == 'IoP':
        for month in shortMonths:
            if month in eventDateList[event]:
                monthIndex = eventDateList[event].index(month)
                eventDateList[event] = eventDateList[event][monthIndex-3:monthIndex +8]
                eventLocationList[event] = eventLocationList[event][monthIndex + 23::]
                break
        exInput(iopSht, iopRowInput)
        iopRowInput +=1
    elif eventInstList[event] == 'ICE':
        exInput(iceSht, iceRowInput)
        iceRowInput +=1
    elif eventInstList[event] == 'IstructE':
        exInput(istructeSht, istructeRowInput)
        istructeRowInput +=1
    elif eventInstList[event] == 'SW Nuclear':
        exInput(swNuclearSht, swNuclearRowInput)
        swNuclearRowInput +=1
        
print("\n\nWebscraping finished")

# ===========================================================================================================================================================
# Updating information from earlier versions

# ===========================================================================================================================================================


msg = "Do you want to update a previous tracker?"
title = "SpyderPig Update"
choices = ["Yes", "No"]
choice = choicebox(msg, title, choices)
if choice == "Yes":
    update = True
else:
    update = False
    print("\nProcess finished")

if update == True:
    msgbox("Please select the old tracker you wish to update")   
    oldTrackerFile = fileopenbox()
    #print(oldTrackerFile)

#Does all the webscraping here or at start of script
#startRowInput = 8 # Note this is for testing and will be deleted when integrated
if update == True:
    print("\nLoading old Data")
    oldWb = xw.Book(oldTrackerFile)
    oldShts = oldWb.sheets
    #print(oldShts)
    oldEvents = []
    oldDates = []
    oldInstitution = []
    oldNoInterested = []
    oldInterestedPeople = []
    for oldSht in range(len(oldShts)):
        shtRowInput = startRowInput
        while True:
            if (oldShts[oldSht].cells(shtRowInput, 1).value) == None and (oldShts[oldSht].cells(shtRowInput + 1, 1).value) == None:
                break
            else:
                oldEvents.append(oldShts[oldSht].cells(shtRowInput, 1).value)
                oldDates.append(oldShts[oldSht].cells(shtRowInput, 4).value)
                oldInstitution.append(oldSht)
                oldNoInterested.append(oldShts[oldSht].cells(shtRowInput, 5).value)
                oldInterestedPeople.append(oldShts[oldSht].cells(shtRowInput, 8).value)
            shtRowInput += 1
    print("\nLoaded old Data")
    print("\nLoading new Data")
    sheets = wb.sheets
    newEvents = []
    newDates = []
    newInstitution = []
    sheetInputRowList = []
    for sheet in range(len(sheets)):
        sheetRowInput = startRowInput
        while True:
            if (sheets[sheet].cells(sheetRowInput, 1).value) == None and (sheets[sheet].cells(sheetRowInput + 1, 1).value) == None:
                break
            else:
                newEvents.append(sheets[sheet].cells(sheetRowInput, 1).value)
                newDates.append(sheets[sheet].cells(sheetRowInput, 4).value)
                sheetInputRowList.append(sheetRowInput)
            sheetRowInput += 1
                
    print("\nLoaded new Data")

    for i in range(len(oldEvents)):
        for j in range(len(newEvents)):
            if newEvents[j] == oldEvents[i] and newDates[j] == oldDates[i] and oldNoInterested != None:
                sheets[oldInstitution[i]].cells(sheetInputRowList[j], 5).value = oldNoInterested[i]
                sheets[oldInstitution[i]].cells(sheetInputRowList[j], 8).value = oldInterestedPeople[i]
                #print('yeet')
                break
    print("Process Finished")
    print("\nPlease saved this version and superseed the previous version")

    

