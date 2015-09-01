#!/usr/bin/env python

import urllib2
import socket
import sys
import re
import optparse

def argParser():
	parser = optparse.OptionParser()
	parser.add_option("-i", dest = 'ipaddr', default = '67.122.193.241', type = 'string', help = 'IP addr')
	parser.add_option("-l", dest = 'logfile', default = 'HW.log', type = 'string', help = 'output log file')
	parser.add_option("-v", action="store_true", dest = 'verbose', help = 'verbose output')
	return parser.parse_args()

class reverseip(object):

           def __init__(self, ipaddr="0"):
               try:
                   name = socket.gethostbyaddr(ipaddr)
                   #print name
               except socket.herror, e:
                   junk="me"

               try:
                   name = socket.getfqdn(ipaddr)
                   print name
               except socket.herror, e:
                   print "No ip Address for ipaddr" ;

if __name__ == '__main__':
     (options, args) = argParser()
     p = reverseip(options.ipaddr)
