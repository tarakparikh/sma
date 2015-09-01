#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
import sqlite3

# Get command line arguments
def argParser():
	parser = optparse.OptionParser()
	parser.add_option("-n", dest = 'jobs_per_node', default = '20', type = 'int', help = 'Number of jobs per node')
	parser.add_option("-l", dest = 'logfile', default = 'HW.log', type = 'string', help = 'output log file')
	parser.add_option("-v", action="store_true", dest = 'verbose', help = 'verbose output')
	#(options, args) = parser.parse_args()
	return parser.parse_args()
#Parser Done

(options, args) = argParser()
print "ARGUMENTS PARSED ",options, args

#Print

sqconn = sqlite3.connect("mystk.db");
sqconn.execute('''CREATE TABLE STOCKS
       (ID INT PRIMARY KEY     NOT NULL,
       SYMBOL           TEXT    NOT NULL,
       PRICE        REAL    NOT NULL,
       SMA        REAL    ,
       SMA50      REAL    );''')

sqconn.execute('''CREATE TABLE COMPANIES
       (ID INT PRIMARY KEY     NOT NULL,
	NAME TEXT 		NOT NULL,
       SYMBOL           TEXT    NOT NULL);''')

sqconn.execute("INSERT INTO STOCKS (ID,SYMBOL,PRICE) \
      VALUES (1, 'MSFT', 100.0 )");

my_tuple_arr = (
	(2, "CSCO", 25.0),
	(3, "INTC", 25.0),
	(4, "JNPR", 25.0)
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
sqconn.executemany("INSERT INTO STOCKS (ID,SYMBOL,PRICE) \
      VALUES (?, ?, ?)", my_tuple_arr);

sqconn.executemany("UPDATE STOCKS SET SMA = ? WHERE ID=?", my_tuple_sma_arr);
sqconn.executemany("UPDATE STOCKS SET SMA50 = ? WHERE ID=?", my_tuple_sma50_arr);

#sqconn.execute("INSERT INTO NEWCOMPANY (ID, NAME,AGE,ADDRESS,SALARY) \
#SELECT ID, NAME,AGE,ADDRESS,SALARY \
#from COMPANY");

sqconn.commit()
print "Records created successfully";
cursor = sqconn.execute("SELECT id, symbol, price, sma, sma50  from STOCKS")
for row in cursor:
   print "ID = ", row[0]
   print "SYMBOL = ", row[1]
   print "PRICE = ", row[2]
   print "SMA = ", row[3]
   print "SMA50 = ", row[4], "\n"

print "Operation done successfully";

#sqconn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
#sqconn.commit
#print "Total number of rows updated :", sqconn.total_changes
#
#cursor = sqconn.execute("SELECT id, name, address, salary  from COMPANY")
#for row in cursor:
   #print "ID = ", row[0]
   #print "NAME = ", row[1]
   #print "ADDRESS = ", row[2]
   #print "SALARY = ", row[3], "\n"
#
#print "Opened database successfully";

#sqconn.execute("DELETE from COMPANY where ID=2;")
#sqconn.commit
#print "Total number of rows deleted :", sqconn.total_changes
#
#cursor = sqconn.execute("SELECT id, name, address, salary  from NEWCOMPANY")
#for row in cursor:
   #print "ID = ", row[0]
   #print "NAME = ", row[1]
   #print "ADDRESS = ", row[2]
   #print "SALARY = ", row[3], "\n"
#
#print "Operation done successfully";
sqconn.close()

print "Connected succesffuly"
