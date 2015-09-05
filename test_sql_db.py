#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
import sqlite3
import sql_db_util


sqconn = sqlite3.connect("mystk.db");
sqconn.execute("INSERT INTO STOCK_PRICES (SYMBOL,VAL) \
      VALUES ('MSFT', 100.0 )");

my_tuple_arr = (
	("CSCO", 25.0),
	("INTC", 25.0),
	("JNPR", 25.0),
	("JNPR", 25.0),
	("JNPR", 25.0),
	("JNPR", 25.0),
	("JNPR", 25.0),
	("JNPR", 25.0)
)

my_tuple_sma_arr = (
	(20.0,1),
	(25.0,2),
	(25.0,3),
	(25.0,4)
)

my_tuple_sma50_arr = (
	(21.0,1),
	(23.0,2),
	(29.0,3),
	(25.0,4)
)
sqconn.executemany("INSERT INTO STOCK_PRICES (SYMBOL,VAL) \
      VALUES (?, ?)", my_tuple_arr);

abc = "MSFT"
myList = [
	20.0,
	25.0,
	23.0,
	24.0
]

my_type_arr_2 = tuple([tuple([abc,row]) for row in myList]);
print my_type_arr_2

sqconn.executemany("INSERT INTO STOCK_PRICES (SYMBOL,VAL) \
      VALUES (?, ?)", my_type_arr_2);

sqconn.commit()
print "Records created successfully";
cursor = sqconn.execute("SELECT id, symbol, val  from STOCK_PRICES")
for row in cursor:
   print "ID = ", row[0]
   print "SYMBOL = ", row[1]
   print "VAL = ", row[2], "\n"

list1 = [
	"MENT",
	20.0,
	25.0,
	23.0,
	24.0
]
write_history_symbol('STOCK_PRICES',list1);
sqconn = sqlite3.connect("mystk.db");
cursor = sqconn.execute("SELECT id, symbol, val  from STOCK_PRICES")
for row in cursor:
   print "ID = ", row[0]
   print "SYMBOL = ", row[1]
   print "VAL = ", row[2], "\n"

list2 = [
	["MENT", 20.0],
	["MSFT", 30.0],
	["CSCO", 40.0],
	["XICO", 50.0],
	["PSFT", 60.0]
]
write_daily_values('STOCK_PRICES',list2);
sqconn = sqlite3.connect("mystk.db");
cursor = sqconn.execute("SELECT id, symbol, val  from STOCK_PRICES")
for row in cursor:
   print "ID = ", row[0]
   print "SYMBOL = ", row[1]
   print "VAL = ", row[2], "\n"

myvals = open_reader('STOCK_PRICES');
for abc in myvals:
	print abc[0];
print "Connected succesffuly"
