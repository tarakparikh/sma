#!/usr/bin/env python


import time
import sys
from datetime import date
import read_portfolio_xml
from symbol_analysis import symbol_analysis
import print_colors

class portfolio_analysis(object):
	def __init__(self,filename,sma_ptr):
		self._filename = filename;
		self._sma_ptr = sma_ptr;

	def _rebalance(self):
		# Rebalance Formula is
		# set all falling trend to 5%
		# For rising trend symbols,
		# 	First set all to equal
		#	For reversal += 2
		#	For accelerating += 2
		#	For sharp	 += 2
		# Now calculate Total and reduce all by same amount as 
		# necessary to get the required total
	        #
		# Currently user defined weights are not implemented.
		# Else, first apply user defined weights to get the starting
		# values and then apply above algorithm
		#
		print "Run portfolio rebalance %s" % (self._filename)
		myPortfolio = read_portfolio_xml.read_portfolio(self._filename)
		myhash = {};
		pctg = {};
		for ix1 in myPortfolio:
			symbol = ix1['symbol'];
			symbolData = symbol_analysis(symbol,self._sma_ptr)
			myhash[symbol] = symbolData

		totalNum = len(myPortfolio)
		totalNumRem = totalNum
		totalPctSoFar = 0;
		for symbol in myhash:
			print symbol
			symbolData = myhash[symbol]
			retString = symbolData._analyze()
			curPct = 0;
			if (symbolData._newTrend and symbolData._reverseTrend):
			    curPct += 2;
			if (symbolData._newTrend and symbolData._trendSpeed):
			    curPct += 2;
			if (symbolData._newTrend and symbolData._trendSlope):
			    curPct += 2;
			pctg[symbol] = curPct;
			totalPctSoFar += curPct
			if (not symbolData._newTrend):
			    pctg[symbol] = 5 ;
			    totalPctSoFar += 5;
			    totalNumRem -= 1;

		DivideEq = int((100 - totalPctSoFar) / totalNumRem)
		for symbol in myhash:
		    if (pctg[symbol] != 5):
			pctg[symbol] += DivideEq 

		for ix1 in myPortfolio:
		    symbol = ix1['symbol'];
		    symbolData = myhash[symbol]
		    print_colors.my_print ( "%2s %2s %s" % (ix1['pctg'],pctg[symbol], symbolData._analyze()),'RED')
		

	def _analysis(self):
		print "Run portfolio analysis %s" % (self._filename)
		myPortfolio = read_portfolio_xml.read_portfolio(self._filename)
		for ix1 in myPortfolio:
			symbol = ix1['symbol'];
			symbolData = symbol_analysis(symbol,self._sma_ptr)
			retString = symbolData._analyze()
			print "%2s %s" % (ix1['pctg'],retString)

