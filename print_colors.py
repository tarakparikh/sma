#!/usr/bin/env python

colors = {}
colors['HEADER'] = '\033[95m'
colors['BLUE'] = '\033[94m'
colors['GREEN'] = '\033[92m'
colors['WARNING'] = '\033[93m'
colors['RED'] = '\033[91m'
colors['ENDC'] = '\033[0m'
colors['BOLD']= "\033[1m"
colors['REG']= "\033[0m"

def my_print( msg, cat='REG'):
    print colors[cat] + msg + colors['ENDC']
 
#my_print(str1,'RED')
#my_print(str1,'BOLD')
#my_print(str1,'REG')
#my_print(str1)
