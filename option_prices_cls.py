#!/usr/bin/python


import yahoostock
import time
import sys
import random
import optparse
from datetime import date

class option_class:
	def __init__(self,symbol,myPrice,mySma,safetyGoal,profitGoal):
                self._symbol = symbol;
                self._price  = float(myPrice);
                self._sma = float(mySma);
		self._sg  = safetyGoal;
		self._pg  = profitGoal;
		self._type = "P";
		self._opt_price = "P";
		self._opt_quote = 0.0;
		self._diffPct = 0;
		self._returnPct = 0;

	def _check_if_relevant(self,myLineArr):
    		type = myLineArr['type']
    		opt_price = float(myLineArr['price'])
    		quote = float(myLineArr['bid_price'])
    		if (type == 'P'):
	 		if (self._price > opt_price):
             			diffVal = self._price - opt_price
             			diffPct = ((self._price - opt_price) / self._price) * 100
             			returnPct = (quote*100)/(opt_price-quote)
             			#print 'DEBUG P %s %f %f %f %.2f %.2f' % (self._symbol, self._price, opt_price,quote,diffPct,returnPct)
	     			#smaDiffPct = abs(opt_price - self._sma)*100 / self._sma
	     			smaDiffPct = 0
             			if (returnPct > self._pg) & (diffPct > self._sg) & (smaDiffPct < self._sg):
                 			self._type = type;
                 			self._opt_price = opt_price
                 			self._opt_quote = quote
                 			self._diffPct = diffPct
                 			self._returnPct = returnPct
		 			return 1
    		else:
	 		if (self._price > opt_price):
             			diffVal = self._price - opt_price
             			diffPct = ((self._price - opt_price) / self._price) * 100
             			returnPct = ((quote-diffVal)*100)/(self._price-quote)
             			#print 'DEBUG %s C %f %f %f %.2f %.2f' % (self._symbol, self._price, opt_price,quote,diffPct,returnPct)
	     			#smaDiffPct = abs(opt_price - self._sma)*100 / self._sma
	     			smaDiffPct = 0
             			if (returnPct > self._pg) & (diffPct > self._sg) & (smaDiffPct < self._sg):
                 			self._type = type;
                 			self._opt_price = opt_price
                 			self._opt_quote = quote
                 			self._diffPct = diffPct
                 			self._returnPct = returnPct
		 			return 1
    		return 0
	

	def _add_to_array(self):
		optArray = {};
		optArray['symbol']    = self._symbol
		optArray['myPrice']   = self._price
		optArray['opt_type']  = self._type
		optArray['opt_price'] = self._opt_price
		optArray['opt_quote'] = self._opt_quote
		optArray['opt_sp']    = self._diffPct
		optArray['opt_pp']    = self._returnPct
		return optArray	

	def _get_relevant_data(self,myArray):
        	retArray = []
        	for ix1 in myArray:
	    		if self._check_if_relevant(ix1):
				retArray.append(self._add_to_array())
        	return retArray 



def get_option_data(symbol, myPrice, mySma, safetyGoal, profitGoal, year, month):
    toRet = []
    myOpt = option_class(symbol,myPrice,mySma,safetyGoal,profitGoal);
    myArray = yahoostock._option_data(symbol,year,month);
    myRetArray = myOpt._get_relevant_data(myArray)
 
    for ix1 in myRetArray:
        symbol = ix1['symbol']
        myPrice = ix1['myPrice']
        opt_type = ix1['opt_type']
        opt_price = ix1['opt_price']
        opt_quote = ix1['opt_quote']
        opt_sp = ix1['opt_sp']
        opt_pp = ix1['opt_pp']
	print '    %4s   %s   %-6.2f   %-6.2f    %-6.2f    %-3.2f  %-3.2f' % (symbol,opt_type,myPrice,opt_price,opt_quote, opt_sp, opt_pp)

    return myRetArray

def call_me(i):
    someArray = ['BRCM', 'XLNX', 'JNPR','NOK','P','ENOC','ALTR','TWC','BRLI','QCOM','ABMD', 'PHMD','CUTR','ARII']
    today =  date.today()
    year =   today.year
    month =  12
    safetyGoal = 7
    profitGoal = 5


    for symbol in someArray:
        myPrice = yahoostock.get_price(symbol)
        getRetArr = get_option_data(symbol,myPrice,myPrice,safetyGoal,profitGoal,year,month)


    sys.exit(0)

#call_me(1)
