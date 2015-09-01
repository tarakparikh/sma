#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time
import sqlite3

def job_status(id):
	logging.debug('Entering function job_status(%s)' % id)
	bsub_cmd = 'bjobs %s' % (id)
	logging.debug('Executing command \'%s\'' % bsub_cmd)
	bsub_out = os.popen(bsub_cmd).readlines()
	# 935611  ecote   DONE  linux_imm  centos-mada mipscs508.m *60_64.sdb Aug 30 12:22
	logging.debug(bsub_out[1])
	match = re.match('%s\s+\w+\s+DONE' % (id), bsub_out[1])
	if match:
		return 1
	else:
		return 0

def do_merge(array, level, x, y):
	logging.debug('Entering function do_merge(array, %s, %s, %s)' % (level, x, y))

	# Create list of coverage files to be merged
	filename = 'ax_coverage_tmp_%0d_%0d_%0d' % (level, x, y)
	logging.debug('Opening file \'%s\'' % filename)
	FILE = open(filename + '.flist', 'w')
	for sdb_file in array[x:y]:
		FILE.write(sdb_file)
	FILE.close()

	# Merge coverage data
	atsim_command = 'atsim +merge_cov_filelist+%s.flist +merge_cov_outfile+%s.sdb' % (filename, filename)
	bsub_cmd = 'bsub -q linux_imm -o %s.log "%s"' % (filename, atsim_command)
	logging.debug('Executing command \'%s\'' % bsub_cmd)
	bsub_out = os.popen(bsub_cmd).readlines()
	match = re.match('Job <(\d+)>', bsub_out[0])
	if match:
		job_id = match.group(1)
		logging.debug('Job ID %s returned' % job_id)
		return job_id
	else:
		sys.stderr.write('Fatal Error: Unable to submit job to grid')
		sys.exit(0)

def parallel_merge(level):
	logging.debug('Entering function parallel_merge(%s)' % level)

	if level == 0:
		filename = 'ax_coverage.sdb'
	else:
		filename = 'ax_coverage_tmp_%0d_*.sdb' % (int(level)-1)


	find_cmd = 'find . -name "%s"' % (filename)
	logging.debug('Executing command \'%s\'' % find_cmd)
	sdb_files = os.popen(find_cmd).readlines()
	sdb_count = len(sdb_files)

	if sdb_count == 1:
		# Save merged coverage file
		copy_cmd = 'cp %s ax_coverage_merged.sdb' % sdb_files[0].rstrip()
		logging.debug('Executing command \'%s\'' % copy_cmd)
		os.popen(copy_cmd)
		# Delete temporary files
		rm_cmd = 'rm -f ax_coverage_tmp*'
		logging.debug('Executing command \'%s\'' % rm_cmd)
		os.popen(rm_cmd)
		return 0
	elif sdb_count == 0:
		logging.error('Fatal Error: Please see log file for more information')
		sys.exit(1)

	# Split the list
	id_list = []
	for i in range(0, sdb_count/options.jobs_per_node):
		x = i*options.jobs_per_node
		y = i*options.jobs_per_node+options.jobs_per_node
		id = do_merge(sdb_files, level, x, y)
		id_list.append(id)

	 # remainder
	x = sdb_count/options.jobs_per_node*options.jobs_per_node
	y = sdb_count
	if (x - y != 0): # corner case
		id = do_merge(sdb_files, level, x, y)
		id_list.append(id)

	# Check status
	while 1:
		all_done = 1
		for id in id_list:
			if job_status(id) == 0:
				all_done = 0
				break
		if all_done == 1:
			break
		time.sleep(10)
	return 1


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

#Logging
logging.basicConfig(filename=options.logfile, filemode='w', level=logging.DEBUG)
if options.verbose:
	logging.info ('HELLO WORKLD %0d' % options.jobs_per_node)
logging.info ('HELLO bbbbdbdbdb %0d' % options.jobs_per_node)
#Logging basics done

name = raw_input('What is your name?\n')
print 'Hi, %s.' % name

friends = ['john', 'pat', 'gary', 'michael']
for i, name in enumerate(friends):
	print "iteration %d is %s" % (i,name)

iter, parents, babies = (1, 1, 1)
while babies < 100:
    print 'This %d generation has %d babies' % (iter, babies)
    iter = iter + 1
    parents, babies = (babies, parents + babies)

#These are arays []
for test_string in ['555-1212', 'ILL-EGAL']:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        print test_string, 'is a valid US local phone number'
    else:
        print test_string, 'rejected'

#These are dictionaries (hash tables) {}
prices = {'apple': 0.40, 'banana': 0.50}
my_purchase = {
    'apple': 1,
    'banana': 6}

#interesting use of sum
grocery_bill = sum(prices[fruit] * my_purchase[fruit]
                   for fruit in my_purchase)
print 'I owe the grocer $%.2f' % grocery_bill
grocery_bill = sum(prices[fruit] * my_purchase[fruit]
                   for fruit in prices)
print 'I owe the grocer $%.2f' % grocery_bill

#try:
#    total = sum(int(arg) for arg in sys.argv[1:])
#    print 'sum =', total
#except ValueError:
#    print 'Please supply integer arguments'

# indent your Python code to put into an email
import glob
# glob supports Unix style pathname extensions
python_files = glob.glob('*.py')
for file_name in sorted(python_files):
    print '    ------' + file_name

    FilePtr = open(file_name)
    for line in FilePtr:
            print '    ' + line.rstrip()

    print

from time import localtime

activities = {8: 'Sleeping',
              9: 'Commuting',
              17: 'Working',
              18: 'Commuting',
              20: 'Eating',
              22: 'Resting' }

time_now = localtime()
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print activities[activity_time]
        break
else:
    print 'Unknown, AFK or sleeping!'

REFRAIN = '''
%d bottles of beer on the wall,
%d bottles of beer,
take one down, pass it around,
%d bottles of beer on the wall!
'''
bottles_of_beer = 99
while bottles_of_beer > 1:
    print REFRAIN % (bottles_of_beer, bottles_of_beer,
        bottles_of_beer - 1)
    bottles_of_beer -= 1

class BankAccount(object):
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount
    def overdrawn(self):
        return self.balance < 0
my_account = BankAccount(15)
my_account.withdraw(5)
print my_account.balance

from itertools import groupby
lines = '''
This is the

first paragraph.

This is the second.
'''.splitlines()
# Use itertools.groupby and bool to return groups of
# consecutive lines that either have content or don't.
for has_chars, frags in groupby(lines, bool):
    if has_chars:
        print ' '.join(frags)
# PRINTS:
# This is the first paragraph.
# This is the second.

import csv

# write stocks data as comma-separated values
writer = csv.writer(open('stocks.csv', 'wb', buffering=0))
writer.writerows([
    ('GOOG', 'Google, Inc.', 505.24, 0.47, 0.09),
    ('YHOO', 'Yahoo! Inc.', 27.38, 0.33, 1.22),
    ('CNET', 'CNET Networks, Inc.', 8.62, -0.13, -1.49)
])

# read stocks data, print status messages
stocks = csv.reader(open('stocks.csv', 'rb'))
status_labels = {-1: 'down', 0: 'unchanged', 1: 'up'}
for ticker, name, price, change, pct in stocks:
    status = status_labels[cmp(float(change), 0.0)]
    print '%s is %s (%s%%)' % (name, status, pct)

BOARD_SIZE = 8

def under_attack(col, queens):
    left = right = col

    for r, c in reversed(queens):
        left, right = left - 1, right + 1

        if c in (left, col, right):
            return True
    return False

def solve(n):
    if n == 0:
        return [[]]

    smaller_solutions = solve(n - 1)

    return [solution+[(n,i+1)]
        for i in xrange(BOARD_SIZE)
            for solution in smaller_solutions
                if not under_attack(i+1, solution)]
for answer in solve(BOARD_SIZE):
    print answer


import itertools

def iter_primes():
     # an iterator of all numbers between 2 and +infinity
     numbers = itertools.count(2)

     # generate primes forever
     while True:
         # get the first number from the iterator (always a prime)
         prime = numbers.next()
	 print prime
         yield prime
	 print "TARAK ",prime

         # this code iteratively builds up a chain of
         # filters...slightly tricky, but ponder it a bit
         numbers = itertools.ifilter(prime.__rmod__, numbers)

for p in iter_primes():
    if p > 1000:
        break
    print "BADRU"
    print p

class BankAccount(object):
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        self.balance -= amount
    def overdrawn(self):
        return self.balance < 0
my_account = BankAccount(15)
my_account.withdraw(5)
print my_account.balance

from ftplib import FTP

class ftpTransfer(object):
	def __init__(self,connectTo="www.athdl.com"):
		self.connection = connectTo
		self.relList = []
		self.lastRel = 0
		self.file = ""

	def handleTransfer(block):
    		self.file.write(block)
    		print ".",
    
#Current Release name format is athdl_linux_RHEL3_5.0_A1_110_19_2012

def findLatest(line):
    match = re.match('.*athdl_linux_RHEL3_5.0_A1_(\d+)_19_2012.*', line)
    if match:
	relList.append(line)


ftp1 = FTP("www.athdl.com")
ftp1.login("athdl","a1t9h9d9l")
ftp1.cwd("RELEASES")
lastRel = 0
relList = [];
ftp1.dir(findLatest)
for rel in relList:
	match = re.match('.*athdl_linux_RHEL3_5.0_A1_(\d+)_19_2012.*', rel)
	if match:
		relNum = match.group(1)
		if (relNum > lastRel):
			lastRel = relNum 

fileList = ftp1.nlst()
#for fname in fileList:
	#print "HELLL ", fname

filename = 'athdl_linux_RHEL3_5.0_A1_%s_19_2012.tgz' % (lastRel)
print "Get ", filename

file = open (filename,'wb')
ftp1.retrbinary('RETR ' + filename, handleTransfer)


ftp1.close()


sys.exit(0)

level = 0
while parallel_merge(level):
	level += 1


