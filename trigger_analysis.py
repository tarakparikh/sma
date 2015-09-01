#!/usr/bin/env python


import time
import sys
from datetime import date
import read_trig_xml
from symbol_analysis import symbol_analysis
import print_colors

trig_case_map = {
}

class trigger_analysis(object):
	def __init__(self,filename,sma_ptr):
		self._filename = filename;
		self._sma_ptr = sma_ptr;

	def _analysis(self):
		print "Run portfolio analysis %s" % (self._filename)
		myTriggers = read_trig_xml.read_triggers(self._filename)
		returnVal = 0
		retArray = [];
		for ix1 in myTriggers:
			symbol = ix1['symbol'];
			symbolData = symbol_analysis(symbol,self._sma_ptr)
			(retType,retString) = symbolData._check_triggers(ix1)
			if (retType == 'T'):
			   returnVal = 1
			#print "%s" % (retString)
			retArray.append(retString)
		return returnVal,retArray
		
