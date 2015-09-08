#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
from datetime import date
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
         TODAY        INTEGER   );''')

    sqconn.execute("INSERT INTO DATETABLE (ID,TODAY) VALUES(1,100)");

    sqconn.execute('''CREATE TABLE COMPANIES
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        NAME TEXT       NOT NULL,
        SYMBOL           TEXT    NOT NULL);''')

    sqconn.commit;
    sqconn.close();

def open_writer():
    sqconn = sqlite3.connect("mystk.db");
    today = date.today()
    today_ordinal = date.toordinal(today)
    my_query_str = "UPDATE DATETABLE SET TODAY = %d WHERE ID=1" % today_ordinal;
    sqconn.execute(my_query_str);
    sqconn.commit()
    sqconn.close();

#
def write_history_symbol (dbname, data):
    sqconn = sqlite3.connect("mystk.db");
    symbol = data[0];
    del data[0];
    data.reverse();
    for row in data:
        print "WRITE ROW ";
        print row;
    my_type_arr_2 = tuple([tuple([symbol,row]) for row in data]);
    print "TUPLE DATA " ;
    print my_type_arr_2;
    my_query_str = "INSERT INTO " + dbname + "(SYMBOL,VAL) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

def write_historical_prices(dbname,allData):
    for priceRow in allData:
        write_history_symbol(dbname,priceRow);

def write_daily_values (dbname, data):
    sqconn = sqlite3.connect("mystk.db");
    my_type_arr_2 = tuple([tuple(row) for row in data]);
    my_query_str = "INSERT INTO " + dbname + "(SYMBOL,VAL) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

def delete_symbol_from_db(dbname,symbol):
    sqconn = sqlite3.connect("mystk.db");
    my_query_str = "DELETE FROM " + dbname + " WHERE SYMBOL='" + symbol + "'";
    sqconn.execute(my_query_str);
    sqconn.commit()
    sqconn.close();

def delete_symbol (dbname, symbol):
    delete_symbol_from_db('STOCK_PRICES',symbol);
    delete_symbol_from_db('STOCK_SMA',symbol);
    delete_symbol_from_db('STOCK_SMA50',symbol);
    delete_symbol_from_db('COMPANIES', symbol);

def write_names (data):
    sqconn = sqlite3.connect("mystk.db");
    my_type_arr_2 = tuple([tuple(row) for row in data]);
    my_query_str = "INSERT INTO COMPANIES (SYMBOL,NAME) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

def open_reader(dbname):
    stocks = [];
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT DISTINCT SYMBOL from STOCK_PRICES")
    for row in cursor:
        rowVal = [];
        symbolName = row[0];
        print symbolName;
        sel_query = "SELECT ID,VAL from " + dbname + " where SYMBOL='" + symbolName + "'";
        #print sel_query;
        symData = sqconn.execute(sel_query);
        for val in symData:
            #print "RETURN DATA ";
            #print val;
            rowVal.append(val[1]);
        rowVal.reverse();
        rowVal.insert(0,symbolName);
        stocks.append(rowVal);
   
    sqconn.close()
    return stocks; 

def open_names():
    stocks = [];
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT SYMBOL,NAME from COMPANIES")
    for row in cursor:
        stocks.append(list(row));
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

