#!/usr/bin/python
import urllib
import re

def _analyze_option_line(data):
    lineData = {} ;
    current_value = 0
    match = re.match(r"^k=(.*)\"><st",data)
    job_id = match.group(1)
    match = re.match(r"^k=.*<b>(.*)</b>",data)
    if match:
        current_value = match.group(1)
    match = re.match(r"^k=.*P00.*",data)
    isPut = "C"
    if match:
        isPut = "P"
    lineData['type'] = isPut
    lineData['price'] = job_id
    lineData['quote'] = current_value
    #print "%s %s %s " % (isPut,job_id,current_value)
    return lineData
    
def _analyze_option_line_2(data):
    lineData = {} ;
    bid_price = 0
    foundLine = 0
    match = re.match(r".*right.>(.*)</td.*right.>(.*)</td.*right.>(.*)</td.*right.>(.*)</td.*",data)
    if match:
        foundLine = 1
        bid_price = match.group(1)
    if (bid_price == "N/A"):
	bid_price = 0
    lineData['bid_price'] = bid_price
    lineData['foundLine'] = foundLine
    #print "%s " % (bid_price)
    return lineData

def _option_data(symbol, year, month):
    lineData = {} ;
    option_data = []
    print_next_line = 0
    url = 'http://finance.yahoo.com/q/op?s=%s&m=%s-%s' % (symbol,year,month)
    somearr =  urllib.urlopen(url).read().strip().strip('"').split(';')
#print 'Options Data for %s , Month %s of %s' % (symbol,month,year)
    for ix in somearr:
        #print ix
        if print_next_line:
 	    tmpData = _analyze_option_line_2(ix)
	    if (tmpData['foundLine']):
	        line_data['bid_price'] = tmpData['bid_price']
	        option_data.append(line_data)
	        print_next_line = 0
        match = re.match(r"^k=(.*)\"><st",ix)
        if match:
            print_next_line = 1
            #option_data.append(_analyze_option_line(ix))
            line_data = _analyze_option_line(ix)
    return option_data

def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')

def __request22(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')
 
def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
 
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]
    return data
 
def get_price(symbol):
    return __request(symbol, 'l1')

def get_multi_price(symbol):
    return __request22(symbol, 'l1')
 
def get_name(symbol):
    return __request(symbol, 'n')

def get_change(symbol):
    return __request(symbol, 'c1')
 
def get_volume(symbol):
    return __request(symbol, 'v')
 
def get_avg_daily_volume(symbol):
    return __request(symbol, 'a2')
 
def get_stock_exchange(symbol):
    return __request(symbol, 'x')
 
def get_market_cap(symbol):
    return __request(symbol, 'j1')
 
def get_book_value(symbol):
    return __request(symbol, 'b4')
 
def get_ebitda(symbol):
    return __request(symbol, 'j4')
 
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')
 
def get_dividend_yield(symbol):
    return __request(symbol, 'y')
 
def get_earnings_per_share(symbol):
    return __request(symbol, 'e')
 
def get_52_week_high(symbol):
    return __request(symbol, 'k')
 
def get_52_week_low(symbol):
    return __request(symbol, 'j')
 
def get_50day_moving_avg(symbol):
    return __request(symbol, 'm3')
 
def get_200day_moving_avg(symbol):
    return __request(symbol, 'm4')
 
def get_price_earnings_ratio(symbol):
    return __request(symbol, 'r')
 
def get_price_earnings_growth_ratio(symbol):
    return __request(symbol, 'r5')
 
def get_price_sales_ratio(symbol):
    return __request(symbol, 'p5')
 
def get_price_book_ratio(symbol):
    return __request(symbol, 'p6')
 
def get_short_ratio(symbol):
    return __request(symbol, 's7')
 
def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
 
    Returns a nested list.
    """
    url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data


def get_price_for_list(symArray):
    lSym = '+'.join(symArray);
    return get_multi_price(lSym).split('\r\n');

#print get_price('^SPX');
#print get_price('GOOG');
#print get_historical_prices('^RUT','20130112','20131012');
#print get_historical_prices('GOOG','20130112','20131012');

#lArray = ['GOOG','MSFT','AAPL'];
#xx = get_price_for_list(lArray)
#print xx
#for i in xx:
#	print i
