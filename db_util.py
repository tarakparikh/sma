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


# 
# Open csv writer for todays date
#
def open_writer(dbname):
    today = date.today()
    today_ordinal = date.toordinal(today)
    fname = "db/stocks." + dbname + "." + "%s" % (today_ordinal) + ".csv"
    print fname
    writer = csv.writer(open(fname, 'wb', buffering=0))
    return writer

#
# Open the last written db file (starting from today) for read
#
def open_reader(dbname):
    today = date.today()
    notOpen = 1
    today_ordinal = date.toordinal(today)
    while notOpen:
        fname = "db/stocks."  + dbname + "." + "%s" % (today_ordinal) + ".csv"
	if os.path.isfile(fname):
            stocks = csv.reader(open(fname, 'rb'))
	    notOpen = 0
        today_ordinal -= 1

    return stocks

#
# Open the specified db file for write
#
def open_writer_fixed(dbname):
    fname = "db/stocks." + dbname + ".csv"
    writer = csv.writer(open(fname, 'wb', buffering=0))
    return writer

#
# Open the specified db file for read
#
def open_reader_fixed(dbname):
    fname = "db/stocks."  + dbname + ".csv"
    stocks = csv.reader(open(fname, 'rb'))
    return stocks

def check_update(dbname):
    today = date.today()
    dbFound = 0
    today_ordinal = date.toordinal(today)
    fname = "db/stocks."  + dbname + "." + "%s" % (today_ordinal) + ".csv"
    if os.path.isfile(fname):
	    dbFound = 1

    return dbFound
    


#writer = csv.writer(open('stocks2.csv', 'wb', buffering=0))
#writer.writerows(someArray2)
