# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 07:57:06 2019

@author: PROL1661
"""

eventDate = '   IoP West Midlands Branch (Keele Centre)     07 Nov 201919:00to20:30   LJ1.75 Lennard Jones Laboratories Keele University ST5 5BG              '
months = ['o'] 
for month in months:
    if month in eventDate:
        monthIndex = eventDate.index(month)
        print(monthIndex)
        eventDate = eventDate[monthIndex-3:monthIndex +8]
        print(eventDate)
        break
    