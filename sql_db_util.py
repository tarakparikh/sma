#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
import sqlite3


#Print

sqconn = sqlite3.connect("mystk.db");
sqconn.execute('''CREATE TABLE STOCK_PRICES
       (ID INT PRIMARY KEY     NOT NULL,
       SYMBOL           TEXT    NOT NULL,
       VAL        REAL    );''')

sqconn.execute('''CREATE TABLE STOCK_SMA
       (ID INT PRIMARY KEY     NOT NULL,
       SYMBOL           TEXT    NOT NULL,
       VAL      REAL    );''')

sqconn.execute('''CREATE TABLE STOCK_SMA50
       (ID INT PRIMARY KEY     NOT NULL,
       SYMBOL           TEXT    NOT NULL,
       VAL      REAL    );''')

sqconn.execute('''CREATE TABLE DATETABLE
       (
       ID INT PRIMARY KEY  NOT NULL,
       PRICE           TEXT    NOT NULL,
       SMA        TEXT    ,
       SMA50      TEXT    );''')

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

#print "Operation done successfully";

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
sqconn.close()

def open_writer(dbname,data):
    sqconn = sqlite3.connect("mystk.db");
    today = date.today()
    today_ordinal = date.toordinal(today)
    fname = "db/stocks." + dbname + "." + "%s" % (today_ordinal) + ".csv"
    print fname
    writer = csv.writer(open(fname, 'wb', buffering=0))
    return writer

#

def open_reader(dataname):
    stocks = [];
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT DISTINCT symbol from STOCKS")
    for row in cursor:
	rowVal = [];
	symbolName = row[0];
	rowVal.append(symbolName);
	symData = sqconn.execute("SELECT VAL from ? where SYMBOL=?",dataname,symbolName);
	for val in symData:
	    rowVal.append(val);
	stocks.append(rowVal);
   
    sqconn.close()
    return stocks; 

def check_update(dbname):
    today = date.today()
    dbFound = 0
    today_ordinal = date.toordinal(today)
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT ? from DateTable",dbname)
    for row in cursor:
	stored_date = row[0];
    if (stored_date == today_ordinal):
	dbFound = 1

    return dbFound

print "Connected succesffuly"
