# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:04:34 2019

@author: PROL1661
"""
import xlwings as xw

wb = xw.Book("CPD Events Tracker Template.xlsm")
sht = wb.sheets['ICE']

sht.cells(8,8).value = "meh"