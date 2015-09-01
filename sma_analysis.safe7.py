#!/usr/bin/env python


import yahoostock
import time
import sys
import random
import optparse
import csv
from datetime import date
import db_util
import mail_intf
import read_portfolio_xml
#import symbol_analysis
#import xml.sax.handler
#import xml.etree.ElementTree as ET
from symbol_analysis import symbol_analysis
from portfolio_analysis import portfolio_analysis
import print_colors

#linewidth = 120

class sma_analysis:
	def __init__(self,analysis_only,update_only,mailit,portfolio_analysis_only,portfolio_file):
		self.analysis_only = analysis_only;
		self.update_only = update_only;
		self.mailit = mailit;
		self.portfolio_analysis_only = portfolio_analysis_only;
		self.portfolio_file = portfolio_file;
                self.priceArray = [];
		self.smaArray = [];
		self.nameArray = [];
		self.splitArr = [];
		self.numSma = 40;

	def _calc_historical_200_day_sma(self,symbol):
		retArray = [];
		prArray = [];
		today = date.today()
		enddate = today.strftime("%Y%m%d")
		today_ordinal = date.toordinal(today)
		start_ordinal = today_ordinal - 380;
		startdate = (date.fromordinal(start_ordinal)).strftime("%Y%m%d")
		#print startdate 
		#print enddate 
		retArray.append(symbol)
		prArray.append(symbol)
		xx = yahoostock.get_historical_prices(symbol,startdate,enddate)

		for i in range (1,241):
	    	    x2 = xx[i];
	    	    prArray.append(x2[1])
	
		for i in range (1,self.numSma+1):
	    	    sma = 0.0
	    	    for mm in range (i,i+200):
			sma += float(prArray[mm]);
	    	    sma = sma / 200.0
	    	    retArray.append(sma)

		return [retArray, prArray]

	def _update_sma_array_to_40_days(self):
		self._open_db()
    		self.smaArray = [];

    		for arr2 in self.priceArray:
		    retArray = [];
		    retArray.append(arr2[0])
		    for i in range (1,self.numSma+1):
	    	        sma = 0.0
	    	        for mm in range (i,i+200):
			    sma += float(arr2[mm]);
	    	        sma = sma / 200.0
	    	        retArray.append(sma)
		    self.smaArray.append(retArray)

    		writer = db_util.open_writer('sma');
    		writer.writerows(self.smaArray);


	def _find_price_list(self,symbol):
    		for ix in self.priceArray:
		    if ix[0] == symbol:
	    		return ix
    		return 0

	def _find_sma_list(self,symbol):
    		for ix in self.smaArray:
		    if ix[0] == symbol:
	    		return ix
    		return 0

	def _find_name(self,symbol):
    		for ix in self.nameArray:
		    if ix[0] == symbol:
	    		return ix[1]
    		return 0

	def _calc_200_day_sma(self,symbol):
		xx = self._find_price_list(symbol)
		x2 = xx[1:201]
		sma = 0.0
		for mm in x2:
			sma += float(mm);
		sma = sma / 200
		return sma

	def _fetch_price(self,symbol):
		return (yahoostock.get_price(symbol))

	def _fetch_historical_data(self,symbol,days):
		today = date.today()
		enddate = today.strftime("%Y%m%d")
		today_ordinal = date.toordinal(today)
		start_ordinal = today_ordinal - days;
		startdate = (date.fromordinal(start_ordinal)).strftime("%Y%m%d")
		retArray = yahoostock.get_historical_prices(symbol,startdate,enddate)
		#print enddate,startdate,retArray
		return retArray

	def populate_name_db(self):
		self.nameArray = []
    		for ix1 in self.smaArray:
		    symbol = ix1[0]
		    name = yahoostock.get_name(symbol)
		    self.nameArray.append([symbol,name])
		writer = db_util.open_writer_fixed('names')
		writer.writerows(self.nameArray)


	def _add_to_sma_db(self,smalist):
    		for ix1 in smalist:
			if self._find_price_list(ix1) == 0:
				print 'Adding ',ix1
	    			[smaVal,priceVal] = self._calc_historical_200_day_sma(ix1);
				name = yahoostock.get_name(ix1)
	    			self.smaArray.append(smaVal)
	    			self.priceArray.append(priceVal)
		    		self.nameArray.append([ix1,name])
	
    		writer = db_util.open_writer('sma');
    		writer.writerows(self.smaArray);
    		writer = db_util.open_writer('price');
    		writer.writerows(self.priceArray);
		writer = db_util.open_writer_fixed('names')
		writer.writerows(self.nameArray)

	def update_price_db(self):
    		stocks = db_util.open_reader('price')
    		self.priceArray = []
    		for arr2 in stocks:
  			newarr = [];
			symbol = arr2[0]
			price = self._fetch_price(symbol)
			print symbol,price
			newarr.append(symbol)
			newarr.append(price)
	    		newarr.extend(arr2[1:240])
			self.priceArray.append(newarr)
     	
    		writer = db_util.open_writer('price');
    		writer.writerows(self.priceArray);

	def update_sma_db(self):
    		stocks = db_util.open_reader('sma')
    		self.smaArray = [];

    		for arr2 in stocks:
  			newarr = [];
			symbol = arr2[0]
			sma = self._calc_200_day_sma(symbol)
			newarr.append(symbol)
			newarr.append(sma)
	    		newarr.extend(arr2[1:self.numSma])
			self.smaArray.append(newarr)
     
    		writer = db_util.open_writer('sma');
    		writer.writerows(self.smaArray);


#
# Here is the flow of this program
#

	def _today_is_market_day(self):
    		retArray = self._fetch_historical_data('GOOG',5)
    		last_quote = retArray[1]
		#print retArray
		last_val = float(last_quote[4])
		last_val_date = last_quote[0].split('-')
		last_date = last_val_date[2]
		today = date.today().day
		cur_val = float(self._fetch_price('GOOG'))
		returnval = 0
		print "Last Val and cur val are %s %s" %(last_val, cur_val)
	        if int(last_date) == int(today):
		     returnval = 1
		     print "TODAY IS LAST DATE %s %s" % (last_date,today)
		else:
		    print "CHeck Last Val and cur val are %s %s" %(last_val, cur_val)
    		    if last_val == cur_val:
        		returnval = 0
    		    else:
		        print "no-match Last Val and cur val are %s %s" %(last_val, cur_val)
        		returnval = 1

		#returnval = 0
		return returnval


	def populate_sma_db(self,smalist):
    		self.priceArray = [];
    		for ix1 in smalist:
			[smaVal,priceVal] = self._calc_historical_200_day_sma(ix1);
			self.smaArray.append(smaVal)
			self.priceArray.append(priceVal)

    		writer = db_util.open_writer('sma');
    		writer.writerows(self.smaArray);
    		writer = db_util.open_writer('price');
    		writer.writerows(self.priceArray);

#
# Update for today if needed
#
	def _open_db(self):
		#
	 	# Open Name Db
		#
		self.nameArray = []
		reader = db_util.open_reader_fixed('names')
		for row in reader:
	    	    self.nameArray.append(row)
		 
		#
	 	# Open Price Db
		#
		self.priceArray = []
		reader = db_util.open_reader('price')
		for row in reader:
	    	    self.priceArray.append(row)

		#
	 	# Open SMA Db
		#
		self.smaArray = []
		reader = db_util.open_reader('sma')
		for row in reader:
	    	    self.smaArray.append(row)

	def update_and_open_db(self):
		if self.analysis_only:
		    self._open_db()
	        else:
		    #
		    #Check if todays price file is created
		    #
		    reader = db_util.open_reader_fixed('names')
		    for row in reader:
	    	        self.nameArray.append(row)
		 
		    if db_util.check_update('price'):
		        print "Found Update"
		        self._open_db()
		    else:
		        #
	    	        # Check if today is a market day
		        #
	    	        if self._today_is_market_day():
		    	    print "TODAY IS MARKET DAY"
			    #
			    # Update Price and SMA DB (opens them too)
			    #
			    self.update_price_db()
			    self.update_sma_db()
	    	        else:
	    	    	    self._open_db()
		
#
# Check for new symbols to be added to db
#	Read symbols file
#       Update price and sma db
#
	def update_symbol_list(self):
    		FilePtr = open('.update_symbols')
    		someArr = [];
    		for line in FilePtr:
        		if line[0] != '#':
	    			someArr.extend (line.strip().split(','))
    		if len(someArr):
       			self._add_to_sma_db(someArr)


	def _read_my_holdings(self):
    		FilePtr = open('.my_holdings')
    		self.holdings = [];
    		for line in FilePtr:
        	    if line[0] != '#':
	    		self.holdings.extend (line.strip().split(','))
	    
	def adjust_splits(self):
    		FilePtr = open('.adjust_splits')
    		splitArr = [];
    		for line in FilePtr:
        		if line[0] != '#':
				newArr = line.strip().split(',')
	    			splitArr.append (newArr)

	def find_in_split_array(self,symbol):
		for row in self.splitArr:
		    if (symbol == row[0]):
			return row
		return 0

	def run_analysis(self):

	    self._read_my_holdings()
	    mail_string = "" ;

	    for row in self.smaArray:
		symbol = row[0]
		symbolData = symbol_analysis(symbol,self)
		retString = symbolData._analyze()

		if symbol in self.holdings:
		    mail_string += '**'
		    mail_string += retString
		    mail_string += '\n'
		else:
		    if (symbolData._reverseTrend | symbolData._crossing):
		        mail_string += retString
		        mail_string += '\n'

		#print retString
		print_colors.my_print (retString,'BOLD')

	    if (self.mailit):
	        mail_intf._send_my_mail(mail_string);
	    return 0


	def run_program(self):
	    self.update_and_open_db()
	    if (self.portfolio_analysis_only):
		portfolio_obj = portfolio_analysis(self.portfolio_file,self)
		portfolio_obj._rebalance()
	    else:
	        if (not self.analysis_only):
		    print "will check update symbol list"
		    self.update_symbol_list()
	        if (not self.update_only):
		    print "will run analysis"
		    self.run_analysis()

	def run_price_check(self,priceRow):
	    symbol = priceRow[0];
	    newRow = []
	    if (find_in_split_arr(symbol)):
	        newRow[0] = symbol
		ratio = find_ratio_in_split_arr(symbol)
	        curPrice = float(priceRow[1])
	        newRow[1] = curPrice
		adjustPrice = 0
	        for i in range(2,len(priceRow)):
		    newPrice = float(priceRow[i]);
		    if adjustPrice:
			newPrice = newPrice * ratio;
		    elif (((abs(curPrice - newPrice))/newPrice) > 0.3):
			adjustPrice = 1
			newPrice = newPrice * ratio;
			    #print "Found Break %s %s %s" % (symbol, curPrice, newPrice)
		    curPrice = newPrice
		    newRow[i] = newPrice
    
	    else:
		newRow.extend(priceRow)

	    print newRow
	    return newRow

	def run_fix_split_checks(self):
	    self._open_db();
	    newPriceArray = []
	    for ix1 in self.priceArray:
		newPriceArray.append(self.run_price_check(ix1))
            writer = db_util.open_writer('price');
    	    writer.writerows(newPriceArray);
	    self._update_sma_array_to_40_days()

	def re_order_based_on_names(self):
	    self._open_db();
	    newPriceArray = []
	    newSmaArray = []
	    for ix1 in self.nameArray:
		newPriceArray.append(self._find_price_list(ix1[0]))
		newSmaArray.append(self._find_sma_list(ix1[0]))

    	    writer = db_util.open_writer('sma');
    	    writer.writerows(newSmaArray)
    	    writer = db_util.open_writer('price');
    	    writer.writerows(newPriceArray)

#
# Run Analysis
#	Check trend direction
#	Check trend reversal
#	Check slope of trend
#	Check 200ma crossing
#	Optionally check 50dma
#

def argParser():
	parser = optparse.OptionParser()
       	#parser.add_option("-n", dest = 'jobs_per_node', default = '20', type = 'int', help = 'Number of jobs per node')
       	#parser.add_option("-l", dest = 'logfile', default = 'HW.log', type = 'string', help = 'output log file')
       	parser.add_option("-m", action="store_true", dest = 'mailit', help = 'mail results')
       	parser.add_option("-r", action="store_true", dest = 'analysis_only', help = 'run analysis only')
       	parser.add_option("-x", action="store_true", dest = 'portfolio_analysis_only', help = 'run portfolio analysis only')
       	parser.add_option("-u", action="store_true", dest = 'update_only', help = 'update only')
       	parser.add_option("-p", dest="portfolio_file", default = '.mgc.xml', type = 'string', help = 'portfolio file for analysis')
	return parser.parse_args()

(options,args) = argParser()
print options

smaobj = sma_analysis(options.analysis_only,options.update_only,options.mailit,options.portfolio_analysis_only,options.portfolio_file)
#smalist = ['GOOG','AAPL']
#smaobj.populate_sma_db(smalist)
#smaobj.populate_name_db()
#smaobj._update_sma_array_to_40_days()
smaobj.run_program()
#smaobj.run_checks()
#smaobj.re_order_based_on_names()

sys.exit(0)
