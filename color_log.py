#!/usr/bin/env python

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

colors = {}
colors['HEADER'] = '\033[95m'
colors['BLUE'] = '\033[94m'
colors['GREEN'] = '\033[92m'
colors['WARNING'] = '\033[93m'
colors['RED'] = '\033[91m'
colors['ENDC'] = '\033[0m'
colors['BOLD']= "\033[1m"
colors['REG']= "\033[0m"

def disable():
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''

def my_print( msg, cat='REG'):
    print colors[cat] + msg + ENDC
 
def infog( msg):
    print OKGREEN + msg + ENDC

def info( msg):
    print OKBLUE + msg + ENDC

def warn( msg):
    print WARNING + msg + ENDC

def err( msg):
    print FAIL + msg + ENDC

def bold( msg):
    print BOLD + msg + ENDC

def hdr( msg):
    print HEADER + msg + ENDC

def regular( msg):
    print ENDC + msg + ENDC

#import log
#log.info("Hello World")
#log.err("System Error")
infog("heheheh")
err("heheheh badd fail")
warn("heheheh badd fail")
bold("heheheh badd fail")
hdr("heheheh badd fail")

xyz = 10;
str1 = "Last Val and cur val are %s" %(xyz)
bold(str1)
regular(str1)
my_print(str1,'RED')
my_print(str1,'BOLD')
my_print(str1,'REG')
my_print(str1)
