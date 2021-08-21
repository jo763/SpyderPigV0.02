# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:13:39 2020

@author: PROL1661
"""

from easygui import *
import xlwings as xw
msg = "Do you want to update a previous tracker?"
title = "SpyderPig Update"
choices = ["Yes", "No"]
choice = choicebox(msg, title, choices)
if choice == "Yes":
    update = True
else:
    update = False

if update == True:
    msgbox("Please select the old tracker you wish to update")   
    oldTrackerFile = fileopenbox()
    print(oldTrackerFile)

#Does all the webscraping here or at start of script
startRowInput = 8 # Note this is for testing and will be deleted when integrated
if update == True:
    oldWb = xw.Book(oldTrackerFile)
    oldShts = oldWb.sheets
    print(oldShts)
    oldEvents = []
    oldDates = []
    oldInstitution = []
    oldNoInterested = []
    for oldSht in range(len(oldShts)):
        shtRowInput = startRowInput
        while True:
            if (oldShts[oldSht].cells(shtRowInput, 1).value) == None and (oldShts[oldSht].cells(shtRowInput + 1, 1).value) == None:
                print('\n==================================================================\n')
                break
            else:
                oldEvents.append(oldShts[oldSht].cells(shtRowInput, 1).value)
                oldDates.append(oldShts[oldSht].cells(shtRowInput, 4).value)
                oldInstitution.append(oldSht)
                oldNoInterested.append(oldShts[oldSht].cells(shtRowInput, 5).value)

                print(oldShts[oldSht].cells(shtRowInput, 1).value)
            shtRowInput += 1
    
