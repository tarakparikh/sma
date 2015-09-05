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

def create_tables():
    sqconn = sqlite3.connect("mystk.db");
    sqconn.execute('''CREATE TABLE STOCK_PRICES
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       SYMBOL           TEXT    NOT NULL,
       VAL        REAL    );''')

    sqconn.execute('''CREATE TABLE STOCK_SMA
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       SYMBOL           TEXT    NOT NULL,
       VAL      REAL    );''')

    sqconn.execute('''CREATE TABLE STOCK_SMA50
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       SYMBOL           TEXT    NOT NULL,
       VAL      REAL    );''')

    sqconn.execute('''CREATE TABLE DATETABLE
       (
       ID INT PRIMARY KEY     NOT NULL,
       TODAY           TEXT    NOT NULL
       );''')

    sqconn.execute('''CREATE TABLE COMPANIES
       (ID INT PRIMARY KEY     NOT NULL,
	NAME TEXT 		NOT NULL,
       SYMBOL           TEXT    NOT NULL);''')

    sqconn.commit;

def open_writer(dbname,data):
    sqconn = sqlite3.connect("mystk.db");
    today = date.today()
    today_ordinal = date.toordinal(today)
    sqconn.execute("UPDATE DATETABLE SET TODAY = ? WHERE ID=1", today_ordinal);
    return writer

#
def write_history_symbol (dbname, data):
    sqconn = sqlite3.connect("mystk.db");
    symbol = data[0];
    del data[0];
    my_type_arr_2 = tuple([tuple([symbol,row]) for row in data]);
    my_query_str = "INSERT INTO " + dbname + "(SYMBOL,VAL) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()

def write_daily_values (dbname, data):
    sqconn = sqlite3.connect("mystk.db");
    my_type_arr_2 = tuple([tuple(row) for row in data]);
    print my_type_arr_2;
    my_query_str = "INSERT INTO " + dbname + "(SYMBOL,VAL) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()

def open_reader(dbname):
    stocks = [];
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT DISTINCT symbol from STOCK_PRICES")
    for row in cursor:
	rowVal = [];
	symbolName = row[0];
	print symbolName;
	rowVal.append(symbolName);
	sel_query = "SELECT VAL from " + dbname + " where SYMBOL='" + symbolName + "'";
	print sel_query;
	symData = sqconn.execute(sel_query);
	for val in symData:
	    rowVal.append(val[0]);
	stocks.append(rowVal);
   
    sqconn.close()
    return stocks; 

def check_update(dbname):
    today = date.today()
    dbFound = 0
    today_ordinal = date.toordinal(today)
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT TODAY from DateTable")
    for row in cursor:
	stored_date = row[0];
    if (stored_date == today_ordinal):
	dbFound = 1

    sqconn.close()
    return dbFound


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

#sqconn.executemany("UPDATE STOCK_PRICES SET SMA = ? WHERE ID=?", my_tuple_sma_arr);
#sqconn.executemany("UPDATE STOCKS SET SMA50 = ? WHERE ID=?", my_tuple_sma50_arr);

#sqconn.execute("INSERT INTO NEWCOMPANY (ID, NAME,AGE,ADDRESS,SALARY) \
#SELECT ID, NAME,AGE,ADDRESS,SALARY \
#from COMPANY");

sqconn.commit()
print "Records created successfully";
cursor = sqconn.execute("SELECT id, symbol, val  from STOCK_PRICES")
for row in cursor:
   print "ID = ", row[0]
   print "SYMBOL = ", row[1]
   print "VAL = ", row[2], "\n"

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
