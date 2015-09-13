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
         DATEVAL    INTEGER,
         SYMBOL           TEXT    NOT NULL,
         VAL        REAL    );''')

    sqconn.execute('''CREATE TABLE STOCK_SMA
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         DATEVAL    INTEGER,
         SYMBOL           TEXT    NOT NULL,
         VAL      REAL    );''')

    sqconn.execute('''CREATE TABLE STOCK_SMA50
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         DATEVAL    INTEGER,
         SYMBOL           TEXT    NOT NULL,
         VAL      REAL    );''')

    sqconn.execute('''CREATE TABLE DATETABLE
       (
         ID INT PRIMARY KEY     NOT NULL,
         TODAY        INTEGER   );''')

    sqconn.execute("INSERT INTO DATETABLE (ID,TODAY) VALUES(1,100)");

    sqconn.execute('''CREATE TABLE COMPANIES
       (
        SYMBOL TEXT PRIMARY KEY       NOT NULL,
        NAME           TEXT    NOT NULL);''')

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
    today = date.today()
    today_ordinal = date.toordinal(today)
    datelist = [];
    numRows = len(data);
    today_ordinal -= numRows;
    for i in range(0,numRows):
        today_ordinal += 1;
        datelist.append(today_ordinal);

    my_type_arr_2 = tuple([tuple([datelist[i],symbol,data[i]]) for i in range (0,numRows)]);
    my_query_str = "INSERT INTO " + dbname + "(DATEVAL, SYMBOL,VAL) VALUES (?, ?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

def write_historical_prices(dbname,allData):
    print "WRITE HISTORY CALLED"
    open_writer();
    for priceRow in allData:
        write_history_symbol(dbname,priceRow);

def _check_if_today_written (today_ordinal):
    sqconn = sqlite3.connect("mystk.db");
    sel_query = "SELECT ID,VAL from STOCK_PRICES  where SYMBOL='GOOG' AND DATEVAL='" + today_ordinal + "'";
    cursor = sqconn.execute(sel_query);
    sqconn.close();
    if (len(cursor)):
        return 1;

    return 0;

def write_daily_values (dbname, data):
    print "WRITE DAILY CALLED"
    open_writer();
    sqconn = sqlite3.connect("mystk.db");
    today = date.today()
    today_ordinal = date.toordinal(today)
    if (_check_if_today_written(today_ordinal)):
        #
        #  Today is written. Update values
        #
        my_type_arr_2 = tuple([tuple([row[1],today_ordinal,row[0]]) for row in data]);
        my_query_str = "UPDATE " + dbname + " SET VAL = ? WHERE DATEVAL=? AND SYMBOL=?";
        sqconn.executemany( my_query_str, my_type_arr_2);
    else:
        #
        # Insert new values
        #
        my_type_arr_2 = tuple([tuple([today_ordinal,row[0],row[1]]) for row in data]);
        my_query_str = "INSERT INTO " + dbname + "(DATEVAL,SYMBOL,VAL) VALUES (?, ?, ?)"
        sqconn.executemany( my_query_str, my_type_arr_2);

    sqconn.commit()
    sqconn.close();

def delete_symbol_from_db(dbname,symbol):
    sqconn = sqlite3.connect("mystk.db");
    my_query_str = "DELETE FROM " + dbname + " WHERE SYMBOL='" + symbol + "'";
    sqconn.execute(my_query_str);
    sqconn.commit()
    sqconn.close();

def delete_db(dbname):
    sqconn = sqlite3.connect("mystk.db");
    my_query_str = "DROP TABLE " + dbname ;
    #sqconn.execute(my_query_str);
    sqconn.execute('''CREATE TABLE COMPANIES
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                    NAME TEXT       NOT NULL,
                            SYMBOL           TEXT    NOT NULL);''')
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
    my_query_str = "INSERT OR IGNORE INTO COMPANIES (SYMBOL,NAME) VALUES (?, ?)"
    sqconn.executemany( my_query_str, my_type_arr_2);
    sqconn.commit()
    sqconn.close();

def get_stock_list():
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT DISTINCT SYMBOL from STOCK_PRICES")
    stocks = list(row[0] for row in cursor);
    sqconn.close()
    return stocks; 

def open_reader(dbname):
    stocks = [];
    sqconn = sqlite3.connect("mystk.db");
    cursor = sqconn.execute("SELECT DISTINCT SYMBOL from STOCK_PRICES")
    for row in cursor:
        rowVal = [];
        symbolName = row[0];
        #print symbolName;
        sel_query = "SELECT VAL from " + dbname + " where SYMBOL='" + symbolName + "'";
        #print sel_query;
        symData = sqconn.execute(sel_query);
        rowVal = list(val[0] for val in symData);
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


def check_update():
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

