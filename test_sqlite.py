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

sqconn = sqlite3.connect("mytest.db");
sqconn.execute('''CREATE TABLE WAVEFORM
       (ID INT PRIMARY KEY     NOT NULL,
	NAME TEXT 		NOT NULL,
       PARENT           TEXT    NOT NULL,
       FIELDNAME        TEXT     NOT NULL,
       STARTTIME        TEXT     NOT NULL);''')

sqconn.execute("INSERT INTO WAVEFORM (ID,NAME,PARENT,FIELDNAME,STARTTIME) \
      VALUES (1, '@seq_item@1', "@Driveer@1, "req", "1000" )");
sqconn.execute("INSERT INTO WAVEFORM (ID,NAME,PARENT,FIELDNAME,STARTTIME) \
      VALUES (2, '@seq_item@2', "@Driveer@1, "req", "1000" )");
sqconn.execute("INSERT INTO WAVEFORM (ID,NAME,PARENT,FIELDNAME,STARTTIME) \
      VALUES (3, '@seq_item@3', "@Driveer@1, "req", "1000" )");
sqconn.execute("INSERT INTO WAVEFORM (ID,NAME,PARENT,FIELDNAME,STARTTIME) \
      VALUES (4, '@seq_item@4', "@Driveer@1, "req", "1000" )");


#sqconn.execute("INSERT INTO NEWCOMPANY (ID, NAME,AGE,ADDRESS,SALARY) \
#SELECT ID, NAME,AGE,ADDRESS,SALARY \
#from COMPANY");

sqconn.commit()
print "Records created successfully";
cursor = sqconn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"

print "Operation done successfully";

sqconn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
sqconn.commit
print "Total number of rows updated :", sqconn.total_changes

cursor = sqconn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"

print "Opened database successfully";

sqconn.execute("DELETE from COMPANY where ID=2;")
sqconn.commit
print "Total number of rows deleted :", sqconn.total_changes

cursor = sqconn.execute("SELECT id, name, address, salary  from NEWCOMPANY")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"

print "Operation done successfully";
sqconn.close()

print "Connected succesffuly"
