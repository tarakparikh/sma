#!/usr/bin/python


import yahoostock
import time
import sys
import random
import optparse
from datetime import date

#linewidth = 120

def get_relevant_data(myPrice,myArray,i):
        retArray = []
#print "My Price is %s" % (myPrice)
        for ix1 in myArray:
            type = ix1['type']
            price = float(ix1['price'])
            quote = float(ix1['quote'])
            if (type == 'P'):
                diffVal = myPrice - price
                diffPct = ((myPrice - price) / myPrice) * 100
                returnPct = (quote/myPrice) * 100 
#print 'DEBUG %s %s %s %s' % (price,quote,diffPct,returnPct)
                if (diffPct > 0.0):
                    if (returnPct > i):
                        quoteArr = {}
                        quoteArr['price'] = price
                        quoteArr['quote'] = quote
                        retArray.append(quoteArr)
#print 'I HAVE %s %s %.2f' % (price,quote,returnPct)
        return retArray 

def get_option_data(symbol, year, month,i):
    myPrice = float(yahoostock.get_price(symbol))
    myArray = yahoostock._option_data(symbol,year,month);
    myRetArray = get_relevant_data(myPrice,myArray,i)
    for ix1 in myRetArray:
        price = ix1['price']
        quote = ix1['quote']
        returnPct = (quote/myPrice) * 100 
        print '    %4s   %-6.2f   %-6.2f    %-6.2f    %-2.2f' % (symbol,myPrice,price,quote, returnPct)

class stock:
	def __init__(self,symbol="MSFT"):
                self.symbol = symbol;
                self.price  = 0.0;
                self.oldPrice = 0.0;
                self.change = 0.0;
                self._update()

	def _update(self):
                self.oldPrice = self.price
                self.price = yahoostock.get_price(self.symbol)
                self.change = yahoostock.get_change(self.symbol) 

	def display(self):
                if ((random.randint(0,100) % 20) == 0):
                        self._update()
                return "%5s %.2f(%.2f)" % (self.symbol , float(self.price), float(self.change))

def printLine(linewidth, s):
        sys.stdout.write(s + " " * (linewidth - len(s)) + "\r")
        sys.stdout.flush()

symbolList = ['GOOG','AAPL','MSFT','CSCO','NOK','P','INTC','^IXIC','^GSPC']

def callMe():
    newsym = raw_input('Enter another symbol or \'0\' to exit\n')
    if (newsym == "0"):
        sys.exit(0)
#symbolList.remove('MSFT')
    symbolList.append(newsym)
    ticker(symbolList)

def argParser():
	parser = optparse.OptionParser()
	parser.add_option("-w", dest = 'linewidth', default = '120', type = 'int', help = 'Ticker Width')
	return parser.parse_args()

		
def ticker(linewidth, symbolList):
        stockArray = [];
        curpos = 0;
        for i,name in enumerate(symbolList):
#print "%d %s" % (i,name)
#print "%d" % (i)
	        stockArray.append (stock(name))

        while 1:
                try:
                        val = "" 
                        for stk in stockArray:
                                val = val + stk.display()
                                val = val + " "
                        if (curpos > len(val)):
                                curpos = 0;
                        newval = val[curpos:curpos+linewidth];
                        if (len(newval) < linewidth):
                                newval = newval + val[0:linewidth-len(newval)-1]
                        printLine(linewidth, newval)
                        curpos = curpos + 20 
                        time.sleep(1)
        
                except KeyboardInterrupt:
#print 'Bye'
                        callMe();
                        sys.exit(0)

#ticker(['GOOG','AAPL','MSFT','CSCO','NOK','P','INTC','^IXIC','^GSPC'])

(options, args) = argParser()
print "ARGUMENTS PARSED ",options, args

someArray = ['IBM', 'BRCM', 'XLNX', 'JNPR','GOOG','AAPL','MSFT','CSCO','NOK','P','INTC','ENOC','BRKB','ALTR','TWC','BRLI','QCOM','SNPS','ORCL']
#ticker(options.linewidth, symbolList)
today =  date.today()
year =   today.year
month =  today.month

for i in range(1,7):
    month = today.month + i
    if (month > 12):
        month -= 12
        year = today.year + 1
    print 'Put Options for %s %s'%(month,year)  
    for symbol in someArray:
        get_option_data(symbol,year,month,i)
    print '----------------------'



#import googlestock
#aapl = googlestock.get_quote('AAPL')
#print aapl

sys.exit(0)
