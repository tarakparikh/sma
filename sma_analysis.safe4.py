#!/usr/bin/python


import yahoostock
import time
import sys
import random
import optparse
import csv
from datetime import date
import db_util
import mail_intf

#linewidth = 120


class symbol_data:
	def __init__(self,symbol,sma_ptr):
		self.symbol = symbol;
		self.sma_ptr = sma_ptr;

class sma_analysis:
	def __init__(self,analysis_only,update_only,mailit):
		self.analysis_only = analysis_only;
		self.update_only = update_only;
		self.mailit = mailit;
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
		last_val = float(last_quote[1])
		last_val_date = last_quote[0].split('-')
		last_date = last_val_date[2]
		today = date.today().day
		cur_val = float(self._fetch_price('GOOG'))
	        if int(last_date) == int(today):
		     return 1
		else:
    		    if last_val == cur_val:
        		return 0
    		    else:
        		return 1


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


	def _slope_calc(self, trend, row):
	    if trend:
		slope = (float(row[0]) - float(row[19]))/20
	    else:
		slope = (float(row[19]) - float(row[0]))/20
	    return slope
		

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

	def _trend_reversal(self, smaRow):
	        symbol = smaRow[0]
	        startSma = float(smaRow[self.numSma])
	        latestSma = float(smaRow[1])
	        trend = 0
		if (startSma < latestSma):
		    trend = 1
	        reverseTrend = 0
		newTrend = trend
		for i in range (7,33):
		     val = float(smaRow[i])
		     if trend: 
			if ((val > latestSma) | (val < startSma)):
			     reverseTrend = 1
			if (val > latestSma):
			     newTrend = 0
			if (val < startSma):
			     newTrend = 1
		     else: 
			if ((val < latestSma) | (val > startSma)):
			     reverseTrend = 1
			if (val < latestSma):
			     newTrend = 1
			if (val > startSma):
			     newTrend = 0

		return trend,reverseTrend,newTrend


	def _price_analysis(self,smaRow):
	    symbol = smaRow[0]
	    curSma = float(smaRow[1])
	    priceRow = self._find_price_list(symbol)
	    curPrice = float(priceRow[1])
	    prevPrice = float(priceRow[2])
	    crossing = 0
	    pctage_diff = 0.0
	    if (curPrice > curSma):
		if (curSma > prevPrice):
			crossing = 1
			#return "%s crossed above 200 day Moving Avg" % (symbol)
		else:
			pctage_diff = ((curPrice - curSma)*100.0) / curPrice
			
	    else:
		if (curSma < prevPrice):
			crossing = 2
			#return "%s crossed below 200 day Moving Avg" % (symbol)
		else:
			pctage_diff = ((curSma - curPrice)*100.0) / curPrice

	    pctage_diff = ((curPrice - curSma)*100.0) / curPrice
	    return crossing,pctage_diff,curPrice,prevPrice

	def _trend_shape(self,trend,smaRow):
		trendSpeed = 0
		trendSlope = 0
		slope_20 =  self._slope_calc(trend, smaRow[1:21])	
		slope_40 =  self._slope_calc(trend, smaRow[21:41])	
	        startSma = float(smaRow[self.numSma])
	        latestSma = float(smaRow[1])
		if trend:
			pctChng = ((latestSma - startSma)*100.0)/latestSma
		else:
			pctChng = ((startSma - latestSma)*100.0)/latestSma
		if (pctChng > 10.0):
		    trendSpeed = 1

		if (slope_20 > slope_40):
		    trendSlope = 1

		return trendSpeed,trendSlope
	
	def run_analysis(self):

	    self._read_my_holdings()
	    mail_string = "" ;
	    for row in self.smaArray:
		symbol = row[0]
		name = self._find_name(symbol)
		(trend,reverseTrend,newTrend) = self._trend_reversal(row)
		(priceCrossing,smadiff,curPrice,prevPrice) = self._price_analysis(row)
		(trendSpeed,trendSlope) = self._trend_shape(trend,row)

		name += " %6s " % (curPrice)
		if (curPrice > prevPrice):
		    name += "+"
		    name += "%.4s" %(curPrice-prevPrice)
		else:
		    name += "-"
		    name += "%.4s" %(prevPrice-curPrice)

		if reverseTrend:
			trendStr = "reverses to "
			if (newTrend):
			    trendStr += "rising"
			else:
			    trendStr += "falling"
		else:
		    if trend:
			trendStr = "rising"
		    else:
			trendStr = "falling"

		if (priceCrossing == 1):
			smaStr = "crossed above 200dma "
		elif (priceCrossing == 2):
			smaStr = "crossed below 200dma "
		else:
			if (smadiff < 0.0):
			    smaStr = "%2s pct below SMA" % (int(smadiff) * -1)
			else:
			    smaStr = "%2s pct above SMA" % (int(smadiff))

		if trendSpeed:
			trendShape = "sharp"
		else:
			trendShape = "slow"

		if trendSlope:
			trendShape += " Accelerating trend "
		else:
			trendShape += " decelerating trend "

		retString = "%-6s %45s %-20s %-23s %s" % (symbol, name, trendStr, smaStr, trendShape)

		if symbol in self.holdings:
		    mail_string += '**'
		    mail_string += retString
		    mail_string += '\n'
		else:
		    if (reverseTrend | priceCrossing):
		        mail_string += retString
		        mail_string += '\n'

		print retString

	    if (self.mailit):
	        mail_intf._send_my_mail(mail_string);
	    return 0

	def run_program(self):
	    self.update_and_open_db()
	    if (not self.analysis_only):
		print "will check update symbol list"
		self.update_symbol_list()
	    if (not self.update_only):
		print "will run analysis"
		self.run_analysis()

	def run_price_check(self,priceRow):
	    symbol = priceRow[0];
	    curPrice = float(priceRow[1])
	    for i in range(2,len(priceRow)):
		newPrice = float(priceRow[i]);
		if (((abs(curPrice - newPrice))/newPrice) > 0.3):
			print "Found Break %s %s %s" % (symbol, curPrice, newPrice)
		curPrice = newPrice

    		writer = db_util.open_writer('sma');
    		writer.writerows(self.smaArray);
    		writer = db_util.open_writer('price');
    		writer.writerows(self.priceArray);

	def run_checks(self):
	    self._open_db();
	    newPriceArray = []
	    for ix1 in self.priceArray:
		newPriceArray.append(self.run_price_check(ix1))

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
       	parser.add_option("-u", action="store_true", dest = 'update_only', help = 'update only')
	return parser.parse_args()

(options,args) = argParser()
print options

smaobj = sma_analysis(options.analysis_only,options.update_only,options.mailit)
#smalist = ['GOOG','AAPL']
#smaobj.populate_sma_db(smalist)
#smaobj.populate_name_db()
#smaobj._update_sma_array_to_40_days()
smaobj.run_program()
#smaobj.run_checks()
#smaobj.re_order_based_on_names()

sys.exit(0)
