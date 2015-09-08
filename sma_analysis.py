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
import threadingCls
from trigger_analysis import  trigger_analysis
#from option_prices_cls import option_class
import  option_prices_cls
import  sql_db_util


#linewidth = 120

class sma_analysis:
    def __init__(self,analysis_only,update_only,mailit,portfolio_analysis_only,portfolio_file,fix_splits,get_options):
        self.analysis_only = analysis_only;
        self.update_only = update_only;
        self.mailit = mailit;
        self.fix_splits = fix_splits;
        self.portfolio_analysis_only = portfolio_analysis_only;
        self.get_options = get_options;
        self.portfolio_file = portfolio_file;
        self.priceArray = [];
        self.smaArray = [];
        self.sma50Array = [];
        self.nameArray = [];
        self.splitArr = [];
        self.numSma = 40;
        self.mail_string = "" ;
        self.retString = {};
        self.interestingResults = {};
        self._symbolData = {};

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
            prArray.append(x2[4])
    
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

            #writer = sql_db_util.open_writer('sma');
            #writer.writerows(self.smaArray);

    def _gen_sma50_array_for_40_days(self,arr2):
        retArray = [];
        retArray.append(arr2[0])
        for i in range (1,self.numSma+1):
            sma = 0.0
            for mm in range (i,i+50):
                sma += float(arr2[mm]);

            sma = sma / 50.0
            retArray.append(sma)

        return retArray

    def _update_sma50_array_to_40_days(self):
        self._open_db()
        self.sma50Array = [];

        for arr2 in self.priceArray:
            self.sma50Array.append(_gen_sma50_array_for_40_days(arr2))

        #writer = db_util.open_writer('sma50');
        #writer.writerows(self.sma50Array);


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

    def _calc_50_day_sma(self,symbol):
        xx = self._find_price_list(symbol)
        x2 = xx[1:51]
        sma = 0.0
        for mm in x2:
            sma += float(mm);
        sma = sma / 50
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
        #writer = db_util.open_writer_fixed('names')
        #writer.writerows(self.nameArray)


    def _populate_all_dbs_for_symbols(self,symbolList):
        sql_db_util.open_writer();
        for ix1 in symbolList:
            if self._find_price_list(ix1) == 0:
                print 'Adding ',ix1
                [smaVal,priceVal] = self._calc_historical_200_day_sma(ix1);
                name = yahoostock.get_name(ix1)
                self.smaArray.append(smaVal)
                self.priceArray.append(priceVal)
                self.nameArray.append([ix1,name])
                sma50arr = self._gen_sma50_array_for_40_days(priceVal);
                self.sma50Array.append(sma50arr);
                sql_db_util.write_historical_prices('stock_sma',[smaVal]);
                sql_db_util.write_historical_prices('stock_prices',[priceVal]);
                sql_db_util.write_historical_prices('stock_sma50',[sma50arr]);
    
        sql_db_util.write_names(self.nameArray);

    def _fetch_updated_prices(self):
        stockArray = sql_db_util.get_stock_list();
        newPriceArray = [];
        symArr = [];
        for arr in stockArray:
            symArr.append(arr)
        totalLen = len(symArr);
        startIndex = 0;

        while ((startIndex +30) < totalLen):
            newPriceArray.extend(yahoostock.get_price_for_list(symArr[startIndex:startIndex+30]));
            startIndex = startIndex + 30;
            print "Fetched Updated prices for %s" % (startIndex);

        if (startIndex < totalLen):
            newPriceArray.extend(yahoostock.get_price_for_list(symArr[startIndex:totalLen]));

        return newPriceArray;

    def update_price_db(self):
        self.priceArray = []
        updatedPriceArray = self._fetch_updated_prices();
        writeArray = [];
        stocks = sql_db_util.open_reader('stock_prices')
        lIndex = 0;
        for arr2 in stocks:
            newarr = [];
            symbol = arr2[0]
            price = updatedPriceArray[lIndex];
            #print symbol,price
            newarr.append(symbol)
            newarr.append(price)
            newarr.extend(arr2[1:240])
            self.priceArray.append(newarr)
            writeArray.append([symbol,price]);
            lIndex = lIndex + 1;
        
        sql_db_util.write_daily_values('stock_prices',writeArray);

    def update_sma_db(self):
        stocks = sql_db_util.open_reader('stock_sma')
        self.smaArray = [];

        writeArray = [];
        for arr2 in stocks:
            newarr = [];
            symbol = arr2[0]
            sma = self._calc_200_day_sma(symbol)
            newarr.append(symbol)
            newarr.append(sma)
            newarr.extend(arr2[1:self.numSma])
            self.smaArray.append(newarr)
            writeArray.append([symbol,sma]);

        sql_db_util.write_daily_values('stock_sma',writeArray);

        writeArray = [];
        stocks = sql_db_util.open_reader('stock_sma50')
        self.sma50Array = [];
        for arr2 in stocks:
            newarr50 = [];
            symbol = arr2[0]
            sma50 = self._calc_50_day_sma(symbol)
            newarr50.append(symbol)
            newarr50.append(sma50)
            newarr50.extend(arr2[1:self.numSma])
            self.sma50Array.append(newarr50)
            writeArray.append([symbol,sma50]);

        sql_db_util.write_daily_values('stock_sma50',writeArray);
     


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

        #returnval = 1
        return returnval


    def populate_sma_db(self,smalist):
        self.priceArray = [];
        for ix1 in smalist:
            [smaVal,priceVal] = self._calc_historical_200_day_sma(ix1);
            self.smaArray.append(smaVal)
            self.priceArray.append(priceVal)

        #writer = db_util.open_writer('sma');
        #writer.writerows(self.smaArray);
        #writer = db_util.open_writer('price');
        #writer.writerows(self.priceArray);

#
# Update for today if needed
#
    def _open_db(self):
        #
        # Open Name Db
        #
        self.nameArray = []
        reader = sql_db_util.open_names();
        for row in reader:
                self.nameArray.append(row)
         
        #
        # Open Price Db
        #
        self.priceArray = []
        reader = sql_db_util.open_reader('stock_prices')
        for row in reader:
                self.priceArray.append(row)

        #
        # Open SMA Db
        #
        self.smaArray = []
        reader = sql_db_util.open_reader('stock_sma')
        for row in reader:
                self.smaArray.append(row)
        #
        # Open 50day SMA
        #
        self.sma50Array = []
        reader = sql_db_util.open_reader('stock_sma50')
        for row in reader:
                self.sma50Array.append(row)

    def _print_dbs(self):
        for row in self.nameArray:
            print row;
        for row in self.priceArray:
            print row;
        for row in self.smaArray:
            print row;
        for row in self.sma50Array:
            print row;

    def update_and_open_db(self):
        if self.analysis_only:
            self._open_db()
        else:
            #
            #Check if todays price file is created
            #
            reader = sql_db_util.open_names();
            for row in reader:
                    self.nameArray.append(row)
         
            if db_util.check_update('stock_prices'):
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
#   Read symbols file
#       Update price and sma db
#
    def update_symbol_list(self):
        FilePtr = open('.update_symbols')
        someArr = [];
        for line in FilePtr:
            if line[0] != '#':
                someArr.extend (line.strip().split(','))
        if len(someArr):
            self._populate_all_dbs_for_symbols(someArr)
 

    def _read_my_holdings(self):
        FilePtr = open('.my_holdings')
        self.holdings = [];
        for line in FilePtr:
            if line[0] != '#':
                self.holdings.extend (line.strip().split(','))
        
    def _read_split_file(self):
        FilePtr = open('.adjust_splits')
        self.splitArr = [];
        for line in FilePtr:
            if line[0] != '#':
                newArr = line.strip().split(',')
                self.splitArr.append (newArr)

    def _find_in_split_arr(self,symbol):
        for row in self.splitArr:
            if (symbol == row[0]):
                return row
        return 0

    def _get_next_index(self):
        self.threadLock.acquire()
        self.numCurIndex += 1;
        tmpInd = self.numCurIndex
        self.threadLock.release()
        return tmpInd
    
    def _analyze_symbol(self,symbol):
        symbolData = symbol_analysis(symbol,self)
        self.retString[symbol] = symbolData._analyze()
        self._symbolData[symbol] = symbolData
        if (symbolData._reverseTrend | symbolData._crossing | (symbolData._daily_chg > 10)):
            self.interestingResults[symbol] = 1
        else:
            self.interestingResults[symbol] = 0

    def _price_check_symbol(self,symbol):
        symbolData = symbol_analysis(symbol,self)
        self.retString[symbol] = symbolData._find_adj()

    def find_tradeable_options(self):
        today = date.today()
        year = today.year 
        month = 12
        safetyGoal = 1
        profitGoal = 7
        self.numRows = len(self.smaArray)
        for index in range(0,self.numRows):
            symbol = self.smaArray[index][0]
            curPrice = self.priceArray[index][1]
            curSma = self.smaArray[index][1]
            getRetArr = option_prices_cls.get_option_data(symbol,curPrice,curSma,safetyGoal,profitGoal,year,month)

        year = today.year  + 1
        month = 1
        safetyGoal = 1
        profitGoal = 7
        self.numRows = len(self.smaArray)
        for index in range(0,self.numRows):
            symbol = self.smaArray[index][0]
            curPrice = self.priceArray[index][1]
            curSma = self.smaArray[index][1]
            getRetArr = option_prices_cls.get_option_data(symbol,curPrice,curSma,safetyGoal,profitGoal,year,month)

    def analysis_called_from_thread(self,threadName):
        #
        # Keep fetching the next symbol needed to work on
        #
        nextInd = self._get_next_index()
        while (nextInd < self.numRows):
            symbol = self.smaArray[nextInd][0]
            #print "%s: %s %s" % (threadName, nextInd, symbol)
            self._analyze_symbol(symbol)
            #self._price_check_symbol(symbol)
            nextInd = self._get_next_index()


    def run_mt_analysis(self, numThreads):

        #
        # Initialize vars
        #
        self._read_my_holdings()
        self.mail_string = "" ;
        self.numCurIndex = -1;
        self.numRows = len(self.smaArray)

        threadingCls.run_threads(numThreads, self, self.analysis_called_from_thread);
        print "All Analysis Done"

        #
        # Collect and print Results
        #
        for index in range(0,self.numRows):
            symbol = self.smaArray[index][0]
            printColor = 'REG'
            if symbol in self.holdings:
                if self.interestingResults[symbol]:
                    self.mail_string += '**' + self.retString[symbol] + '\n'
                    printColor = 'BOLD'

        print_colors.my_print (self.retString[symbol],printColor)

        #
        # Mail results if necessary
        #
        (retVal,retArr) = self._run_triggers()
        if retVal:
            for trig1 in retArr:
                self.mail_string += '*TRIG*' + trig1 + '\n'
        if (self.mailit):
            mail_intf._send_my_mail(self.mail_string);
        return 0

    def _run_triggers(self):
        #trig  = trigger_analysis('.trig.xml',self)
        #(retVal,retArr) = trig._analysis()
        #return retVal,retArr
        return 0,0
 
    def run_analysis(self):

        self._read_my_holdings()
        self.mail_string = "" ;

        numSyms = len(self.smaArray)
        #for row in self.smaArray:
        for index  in range(0,numSyms):
            symbol = self.smaArray[index][0]
            symbolData = symbol_analysis(symbol,self)
            retString = symbolData._analyze()

            if symbol in self.holdings:
                self.mail_string += '**'
                self.mail_string += retString
                self.mail_string += '\n'
            else:
                if (symbolData._reverseTrend | symbolData._crossing):
                    self.mail_string += retString
                    self.mail_string += '\n'

        #print retString
            print_colors.my_print (retString,'BOLD')

            if (self.mailit):
                mail_intf._send_my_mail(self.mail_string);
        return 0

    def create_50day_sma(self):
        self._update_sma50_array_to_40_days()

    def run_program(self):
        if (self.fix_splits):
            self.run_fix_split_checks()
        else:
            self.update_and_open_db()
            if (self.portfolio_analysis_only):
                portfolio_obj = portfolio_analysis(self.portfolio_file,self)
                portfolio_obj._rebalance()
            elif (self.get_options):
                print "Get Options"
                self.find_tradeable_options()
            else:
                if (not self.analysis_only):
                    print "will check update symbol list"
                    self.update_symbol_list()
                if (not self.update_only):
                    print "will run analysis"
                    #self.run_analysis()
                    self.run_mt_analysis(10)

    def run_price_check(self,priceRow):
        symbol = priceRow[0];
        newRow = []
        if (self._find_in_split_arr(symbol)):
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

    def adj_row_price(self,priceRow):
        symbol = priceRow[0];
        if (self._find_in_split_arr(symbol)):
            symbolData = symbol_analysis(symbol,self)
            return symbolData._adj_price()

        return priceRow

    def run_fix_split_checks(self):
        self.update_and_open_db()
        newPriceArray = []
        self._read_split_file()
        for ix1 in self.priceArray:
            newPriceArray.append(self.adj_row_price(ix1))
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
#   Check trend direction
#   Check trend reversal
#   Check slope of trend
#   Check 200ma crossing
#   Optionally check 50dma
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
    parser.add_option("-f", action="store_true", dest="fix_splits", help = 'Adjustments Price for Splits/Distro')
    parser.add_option("-o", action="store_true", dest="get_options", help = 'Get Option Prices')
    return parser.parse_args()

(options,args) = argParser()
print options

smaobj = sma_analysis(options.analysis_only,options.update_only,options.mailit,options.portfolio_analysis_only,options.portfolio_file,options.fix_splits,options.get_options)
#smalist = ['GOOG','AAPL']
#smaobj.populate_sma_db(smalist)
#smaobj.populate_name_db()
#smaobj._update_sma_array_to_40_days()
smaobj.run_program()
#smaobj.create_50day_sma()
maobj.run_checks()
#smaobj.re_order_based_on_names()
#sql_db_util.create_tables();
#smaobj._open_db()
#smaobj.update_symbol_list()
#smaobj._print_dbs()

sys.exit(0)
