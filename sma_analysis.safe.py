#!/usr/bin/python


import yahoostock
import time
import sys
import random
import optparse
import csv
from datetime import date
import db_util

#linewidth = 120

priceArray = [];

class stock:
	def __init__(self,symbol="MSFT"):
                self.symbol = symbol;
                self.price  = 0.0;
                self.oldPrice = 0.0;
                self.change = 0.0;
		self.sma200 = 0.0;
                self._update()

	def _update(self):
                self.oldPrice = self.price
                self.price = yahoostock.get_price(self.symbol)
                self.change = yahoostock.get_change(self.symbol) 
		self.sma200 = yahoostock.get_200day_moving_avg(self.symbol);

	def display(self):
                if ((random.randint(0,100) % 20) == 0):
                        self._update()
                print "%5s %.2f  %.2f" % (self.symbol , float(self.price), float(self.sma200))

def _calc_historical_200_day_sma(symbol):
	retArray = [];
	priceArray = [];
	today = date.today()
	enddate = today.strftime("%Y%m%d")
	today_ordinal = date.toordinal(today)
	start_ordinal = today_ordinal - 350;
	startdate = (date.fromordinal(start_ordinal)).strftime("%Y%m%d")
	#print startdate 
	#print enddate 
	retArray.append(symbol)
	priceArray.append(symbol)
	xx = yahoostock.get_historical_prices(symbol,startdate,enddate)
	for i in range (1,241):
	    x2 = xx[i];
	    priceArray.append(x2[1])

	for i in range (1,30):
	    sma = 0.0
	    for mm in (i,i+200):
		sma += float(priceArray[i]);
	    sma = sma / 200
	    retArray.append(sma)

	return [retArray, priceArray]

def _find_price_list(symbol):
    for ix in priceArray:
	if ix[0] == symbol:
	    return ix
    return ix

def _calc_200_day_sma(symbol):
	xx = _find_price_list(symbol)
	x2 = xx[1:201]
	sma = 0.0
	for mm in x2:
		sma += float(mm);
	sma = sma / 200
	return sma

def _fetch_200_day_sma(symbol):
	return (yahoostock.get_200day_moving_avg(symbol))

def _fetch_price(symbol):
	return (yahoostock.get_price(symbol))

def _fetch_historical_200_day_ema(symbol):
	retArray = [];
	retArray.append(symbol)
	today = date.today()
	enddate = today.strftime("%Y%m%d")
	today_ordinal = date.toordinal(today)
	start_ordinal = today_ordinal - 60;
	startdate = (date.fromordinal(start_ordinal)).strftime("%Y%m%d")
	#print startdate 
	#print enddate 
	ema = float(_fetch_200_day_sma(symbol));
	retArray.append(ema)
	xx = yahoostock.get_historical_prices(symbol,startdate,enddate)
	mult = 0.004975
	one_minus_mult = 1 - float(mult);

	for i in range (1,30):
	    x2 = xx[i];
	    price = float (x2[1]);
	    print ema,price,mult,one_minus_mult
	    newema = (ema - price*mult)/one_minus_mult;
	    retArray.append(newema)
	    ema = newema

	return retArray


def _populate_sma_db(smalist):
    smaArray = [];
    priceArray = [];
    for ix1 in smalist:
	[smaVal,priceVal] = _calc_historical_200_day_sma(ix1);
	smaArray.append(smaVal)
	priceArray.append(priceVal)
    writer = db_util.open_writer('sma');
    writer.writerows(smaArray);
    writer = db_util.open_writer('price');
    writer.writerows(priceArray);

def _populate_ema_db(emalist):
    someArray = [];
    for ix1 in emalist:
	someArray.append(_fetch_historical_200_day_ema(ix1))
    writer = db_util.open_writer('ema');
    writer.writerows(someArray);

def _populate_price_db():
    someArray = [];
    for ix1 in emalist:
	someArray.append(_fetch_historical_200_day_ema(ix1))
    writer = db_util.open_writer('ema');
    writer.writerows(someArray);

def update_price_db():
    stocks = db_util.open_reader('price')
    priceArray = []
    for arr2 in stocks:
  	newarr = [];
	symbol = arr2[0]
	price = _fetch_price(symbol)
	newarr.append(symbol)
	newarr.append(price)
	for i in range(1,239):
	    newarr.append(arr2[i])
	priceArray.append(newarr)
     
    writer = db_util.open_writer('price');
    writer.writerows(priceArray);

def update_sma_db():
    stocks = db_util.open_reader('sma')
    writeArray = [];

    if len(priceArray) == 0:
	update_price_db()

    for arr2 in stocks:
  	newarr = [];
	symbol = arr2[0]
	sma = _calc_200_day_sma(symbol)
	newarr.append(symbol)
	newarr.append(sma)
	for i in range(1,29):
	    newarr.append(arr2[i])
	writeArray.append(newarr)
     
    writer = db_util.open_writer('sma');
    writer.writerows(writeArray);

#update_sma_db()

#someArray.append(_calc_historical_200_day_sma('FLATX'))
#someArray.append(_calc_historical_200_day_sma('HHBUX'))
#someArray.append(_calc_historical_200_day_sma('SFENX'))
#someArray.append(_calc_historical_200_day_sma('OAKIX'))
#someArray.append(_calc_historical_200_day_sma('UOPIX'))
#someArray.append(_calc_historical_200_day_sma('XLE'))
#print someArray

#stocks = db_util.open_reader('sma');
#for  arr2 in stocks:
	#print arr2

symbolList = ['OAKIX']
#symbolList = ['GOOG','AAPL','FB','LNKD','YHOO','YELP','MSFT','ORCL',
#'CSCO','JNPR','FFIV','JDSU','CIEN','HPQ','CRM','VMW','AMZN',
#'NOK','P','T','VZ','IBM','S',
#'INTC','BRCM','QCOM','ALTR','TXN','XLNX','CAVM','MU','NVDA','AMD','TSM','OVTI','SNDK',
#'SNPS','MENT','CDNS',
#'ABMD','BRLI','BIIB','PHMD','CUTR','PFE','MRK','ABT','LLY',
#'BRKA','GLD','PG','JNJ','ARII','TWC',
#'GPS','WMT','TGT','WAG','HD','AAN','COST',
#'KO','PEP','YUM','MCD',
#'ELON','ERII','ABTL','LOV','ENOC','ABTL',
#'FLATX', 'SFENX','OAKIX'
#]
smaSymbolList = ['AEPGX', 'AMCPX', 'AMRMX', 'APHIX', 'ARTVX', 'BCSIX', 'BERWX', 'BFGFX', 'BUFTX', 'CAAPX', 'CSO', 'CSRSX', 'DEFIX', 'DODFX', 'DODIX', 'DXRLX', 'EXES', 'FAMVX', 'FLATX', 'FMIHX', 'FPNIX', 'FPPFX', 'FSIIX', 'HABDX', 'HHBUX', 'JENHX', 'LSBRX', 'MCHFX', 'MGOYX', 'MINDX', 'MWHYX', 'NAESX', 'NBRFX', 'NEWFX', 'OAKIX', 'OAKIXGURU', 'PENNX', 'POAGX', 'PRDMX', 'PRFDX', 'PRGFX', 'PRIDX', 'PRMSX', 'PRNEX', 'PRNHX', 'PRSVX', 'PRTXX', 'PRWCX', 'PTTRX', 'RERGX', 'RYTRX', 'SFENX', 'SLASX', 'SSHFX', 'SSIFXRGAGX', 'SWPPX', 'SWTSX', 'TPINX', 'TRBCX', 'TRRBX', 'UMBWX', 'UOPIX', 'VBISX', 'VBMFX', 'VBTIX', 'VEIEX', 'VEVIX', 'VEY', 'VFORX', 'VFSVX', 'VGSIX', 'VGTSZ', 'VIMSX', 'VINIX', 'VIPSZ', 'VMGRX', 'VSCIX', 'VTENX', 'VTHRX', 'VTSNX', 'VTTHX', 'VTTSX', 'VTU', 'VTXVX', 'VWELX', 'VWIGX', 'VWITX', 'VWNFX', 'WAAEX', 'WEHIX', 'YAFFX']
emaSymbolList = ['AAN', 'AAPL', 'ABMD', 'ABT', 'ABTL', 'ADRE', 'ALFA', 'ALTR', 'AMD', 'AMJ', 'AMLP', 'AMZN', 'ANGL', 'ARII', 'AXTE', 'BIB', 'BIIB', 'BND', 'BRCM', 'BRKA', 'BRLI', 'BSJF', 'BSJG', 'BSJH', 'BSJI', 'BSV', 'CAVM', 'CDNS', 'CGW', 'CHLC', 'CIEN', 'COST', 'CRM', 'CROC', 'CSCO', 'CSD', 'CURE', 'CUTR', 'DBB', 'DBC', 'DBEF', 'DBJP', 'DBP', 'DBU', 'DGL', 'DHS', 'DISH', 'DLN', 'DSLV', 'DUST', 'DWAS', 'ECON', 'EDEN', 'EELV', 'ELON', 'EMB', 'EMDI', 'EMHY', 'EMLP', 'ENOC', 'ERII', 'EUSA', 'EWGS', 'EWUS', 'FB', 'FCAN', 'FEMS', 'FEP', 'FFIV', 'FINU', 'FJP', 'FKU', 'FLRN', 'FNK', 'FNY', 'FRAK', 'FSZ', 'FVD', 'FWDD', 'FXO', 'FXU', 'FYC', 'FYT', 'GBF', 'GIVE', 'GLD', 'GMFS', 'GOOG', 'GPS', 'GSG', 'HD', 'HDV', 'HECO', 'HPQ', 'HUSE', 'HYLD', 'HYS', 'IAI', 'IAK', 'IAT', 'IAU', 'IBM', 'IDU', 'IGE', 'IHE', 'IHF', 'IIF', 'INTC', 'ITR', 'IWM', 'IXJ', 'IYE', 'IYG', 'IYH', 'JDSU', 'JNJ', 'JNPR', 'JXI', 'KBE', 'KBWB', 'KBWI', 'KBWP', 'KBWR', 'KNOW', 'KO', 'KRE', 'LLY', 'LNKD', 'LOV', 'MCD', 'MCHI', 'MENT', 'MLPA', 'MLPG', 'MLPI', 'MLPN', 'MOAT', 'MRK', 'MSFT', 'MU', 'NFLX', 'NKY', 'NOK', 'NVDA', 'OIH', 'ORCL', 'OVTI', 'P', 'PALL', 'PCY', 'PEP', 'PFE', 'PFI', 'PG', 'PGJ', 'PHMD', 'PID', 'PJP', 'PPLT', 'PRF', 'PSCC', 'PSCE', 'PSCF', 'PSCM', 'PTH', 'PUI', 'PWV', 'PXE', 'PXI', 'PXLV', 'QCOM', 'RFG', 'RHS', 'RPG', 'RSP', 'RTM', 'RWR', 'RWX', 'RXI', 'RYF', 'RYU', 'S', 'SBV', 'SCHA', 'SCHB', 'SCHC', 'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHH', 'SCHV', 'SCHX', 'SDOG', 'SDY', 'SGOL', 'SIVR', 'SJNK', 'SKYY', 'SLY', 'SNDK', 'SNPS', 'SOCL', 'SPGH', 'T', 'TGT', 'TILT', 'TIP', 'TSM', 'TTFS', 'TTT', 'TWC', 'TXN', 'TZW', 'TZY', 'UGA', 'UPW', 'URTH', 'VB', 'VBK', 'VBR', 'VDE', 'VEA', 'VEU', 'VFH', 'VGK', 'VHT', 'VMW', 'VNQ', 'VO', 'VONE', 'VOO', 'VPL', 'VPU', 'VQT', 'VSPY', 'VT', 'VTI', 'VTWO', 'VWO', 'VXUS', 'VZ', 'WAG', 'WMT', 'XAR', 'XBI', 'XHE', 'XHS', 'XLE', 'XLF', 'XLNX', 'XLU', 'XLV', 'XOP', 'XSW', 'XTN', 'YELP', 'YHOO', 'YINN', 'YUM', 'ZIV']

#_populate_sma_db(smaSymbolList);
#_populate_ema_db(emaSymbolList);

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

		
def display_sma(symbolList):
        stockArray = [];
        curpos = 0;
        for i,name in enumerate(symbolList):
#print "%d %s" % (i,name)
#print "%d" % (i)
	     stockArray.append (stock(name))

        for stk in stockArray:
            stk.display()

(options, args) = argParser()
print "ARGUMENTS PARSED ",options, args

#display_sma(symbolList)


sys.exit(0)
