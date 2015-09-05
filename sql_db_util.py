#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
import sqlite3


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
    sqconn.close();

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
    sqconn.close();

def write_daily_values (dbname, data):
    sqconn = sqlite3.connect("mystk.db");
    my_type_arr_2 = tuple([tuple(row) for row in data]);
    print my_type_arr_2;
    my_query_str = "INSERT INTO " + dbname + "(SYMBOL,VAL) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

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

