#!/usr/bin/env python

import logging
import optparse
import os
import re
import subprocess
import sys
import time

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

logging.basicConfig(filename='.parallel_merge.log', filemode='w', level=logging.DEBUG)

# Get command line arguments
parser = optparse.OptionParser()
parser.add_option("-n", dest = 'jobs_per_node', default = '20', type = 'int', help = 'Number of jobs per node')
(options, args) = parser.parse_args()

level = 0
while parallel_merge(level):
	level += 1


