#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
from datetime import date
import csv
import yahoostock
import xml.etree.ElementTree as ET
import sys


#today = date.today()
#today_ordinal = date.toordinal(today)
#print today 
#print today_ordinal
#today_ordinal -= 1
#fname = "stocks." + "%s" % (today_ordinal) + ".csv"
#print fname


#someArray = [];
#someArray.append(("hello", "world"))
#someArray.append (("why", "me"))

#someArray2 = [];
# write stocks data as comma-separated values
#writer = csv.writer(open('stocks.csv', 'wb', buffering=0))
#writer.writerows([
    #('GOOG', 'Google, Inc.', 505.24, 0.47, 0.09),
    #('YHOO', 'Yahoo! Inc.', 27.38, 0.33, 1.22),
    #('CNET', 'CNET Networks, Inc.', 8.62, -0.13, -1.49)
#])

#arr2 = []

#writer.writerows(someArray)
# read stocks data, print status messages
#stocks = csv.reader(open('stocks.csv', 'rb'))
#status_labels = {-1: 'down', 0: 'unchanged', 1: 'up'}
#for  arr2 in stocks:
    #status = status_labels[cmp(float(change), 0.0)]
    #print len(arr2)
    #someArray2.append(arr2);
    #print arr2
    #for ix1 in arr2:
#	print ix1

def open_writer():
    today = date.today()
    today_ordinal = date.toordinal(today)
    fname = "stocks." + "%s" % (today_ordinal) + ".csv"
    print fname
    writer = csv.writer(open(fname, 'wb', buffering=0))
    return writer

def open_reader():
    today = date.today()
    notOpen = 1
    today_ordinal = date.toordinal(today)
    while notOpen:
        today_ordinal -= 1
        fname = "stocks." + "%s" % (today_ordinal) + ".csv"
	if os.path.isfile(fname):
            stocks = csv.reader(open(fname, 'rb'))
	    notOpen = 0

    return stocks


#writer = csv.writer(open('stocks2.csv', 'wb', buffering=0))
#writer.writerows(someArray2)

#xx = yahoostock.get_historical_prices('ABT','20120905','20130909')
#print xx
#last_quote = xx[1]
#last_date = last_quote[0].split('-');
#day = last_date[2];
#today = date.today().day
#print int(day),int(today)

#FilePtr = open('.update_symbols')
#someArr = [];
#for line in FilePtr:
     #if line[0] != '#':
	#someArr.extend (line.strip().split(','))
#if len(someArr):
   ##_add_to_sma_db(someArr)
    #print someArr

#def _part_arr(row):
	#print row
#
#someArr = [];
#for i in range (0,31):
	#someArr.append(i)
#
#_part_arr(someArr[15:31])
#xmlroot = ET.parse("hello.xml")
#treeroot = xmlroot.getroot()
#for child in treeroot:
	#print child.tag,child.attrib
	#for mm in child:
		#print mm.tag,mm.attrib,mm.text


FilePtr = open('.my_holdings')
holdings = [];
for line in FilePtr:
            if line[0] != '#':
		holdings.extend (line.strip().split(','))

#for ix in holdings:
		#print ix


#import elementtree.ElementTree as ET

# build a tree structure
#root = ET.Element("html")

#head = ET.SubElement(root, "head")

#title = ET.SubElement(head, "title")
#title.text = "Page Title"

#body = ET.SubElement(root, "body")
#body.set("bgcolor", "#ffffff")

#body.text = "Hello, World!"

# wrap it in an ElementTree instance, and save as XML
#tree = ET.ElementTree(root)
#tree.write("page.xhtml")

def read_portfolio(filename):
    xmlroot = ET.parse(filename)
    treeroot = xmlroot.getroot()
    myarray = []
    for stock in treeroot:
	    #print stock
	    #print stock.get('symbol')
	    myhash = {};
	    myhash['symbol'] = stock.get('symbol')
	    for mm in stock:
		    myhash[mm.tag] = mm.text
	    myarray.append(myhash)

    return myarray
    

#myportfolio = read_portfolio(".mgc.xml")
#for ix1 in myportfolio:
#	    print ix1
#

def func2(funcname):
    mmm = _afunc
    mmm()
    mmm = funcname
    mmm()

def _afunc():
	print "Hello"

func2 (_afunc)
