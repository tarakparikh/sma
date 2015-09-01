#!/usr/bin/python


import yahoostock
import time
import sys
import random
import optparse
import csv
from datetime import date
import db_util

def _checkSymbols(symbolList):
	retArray = list (sorted(set(symbolList)));
	retSmaArray = []
	retEmaArray = []
	for ix in retArray:
		sma = yahoostock.get_200day_moving_avg(ix)
		if sma == "N/A":
			retSmaArray.append(ix)
		else:
			retEmaArray.append(ix)

	return [retSmaArray, retEmaArray]

symbolList = ['GOOG','AAPL','FB','LNKD','YHOO','YELP','MSFT','ORCL',
'CSCO','JNPR','FFIV','JDSU','CIEN','HPQ','CRM','VMW','AMZN',
'NOK','P','T','VZ','IBM','S',
'INTC','BRCM','QCOM','ALTR','TXN','XLNX','CAVM','MU','NVDA','AMD','TSM','OVTI','SNDK',
'SNPS','MENT','CDNS',
'ABMD','BRLI','BIIB','PHMD','CUTR','PFE','MRK','ABT','LLY',
'BRKA','GLD','PG','JNJ','ARII','TWC',
'GPS','WMT','TGT','WAG','HD','AAN','COST',
'KO','PEP','YUM','MCD',
'ELON','ERII','ABTL','LOV','ENOC','ABTL',
'FLATX', 'SFENX','OAKIX'
'GURU','FINU','ALFA','CROC','SCHD','VSPY','KNOW','DHS','FVD','DLN',
'NFLX','DISH',
'XSW','FNK','FYT','PSCC','FYC','FNY','PXLV','RHS','FWDD','KBWP',
'EDEN','EWUS','EWGS','FKU','DBJP','FSZ','DBEF','FJP','FEP','FCAN',
'DWAS','SDOG','MOAT','XAR','KBWR','HUSE','TTFS','KBWB','TILT',
'KBWI',
'KRE','PFI','FXO','RYF','IAT','IYG','KBE','XLF','IYG','VFH',
'PALL','DUST','SPGH','SBV','IAU','SGOL','GLD','PPLT','DGL','DBP',
'ANGL','TTT','HYLD','BSJI','HYS','BSJH','BSJG','SJNK','ZIV','BSJF',
'HECO','NKY','URTH','SKYY','SOCL','TZY','GIVE','HDV','TZW','RXI',
'FRAK','EMLP','AMLP','MLPA','PXE','UGA','PXI','CGW','XLE','IYE',
'XHS','VHT','XLV','IYH','XHE','CURE','IHF','PTH','IHE','IXJ',
'UPW','XTN','RYU','PUI','FXU','VPU','IDU','XLU','JXI','DBU',
'VT',
'CHLC',
'GMFS',
'FEMS',
'AXTE',
'EMDI',
'EMB',
'ECON',
'PCY',
'EELV',
'EUSA','VONE','SCHX',
'SCHE','ADRE','EMHY',
'SCHH','RWR','VNQ',
'SLY','VTWO','SCHA',
'DBB','GSG','DBC',
'PGJ','MCHI',
'FLRN','ITR','GBF',
'VDE','EXES','XLE',
'AMRMX','SSHFX','PRFDX','VWNFX','FMIHX','SLASX','AMCPX','JENHX',
'TRBCX','DEFIX','CAAPX','WEHIX','FAMVX','FPPFX','POAGX','PRDMX',
'BERWX','PENNX','RYTRX','PRSVX','WAAEX',
'CSRSX','PRNEX',
'AEPGX','DODFX','OAKIX','UMBWX','VWIGX','PRIDX','NEWFX','PRMSX',
'DODIX','HABDX','FPNIX','LSBRX','MWHYX','VIPSZ','VWITX','TPINX',
'SWPPX','SWTSX','VIMSX','NAESX',
'FSIIX','VGTSZ','VFSVX','VEIEX','VGSIX',
'VBMFX','VBISX',
'PRWCX','VWELX','TRRBX','VTTHX',
'VOO','VTI',
'VO','VB','VBR',
'VEA','VEY','VWO',
'PID','SDY','IGE','RWX','VNQ',
'BND','BSV','TIP',
'BIB','DSLV','YINN',
'SCHX','SCHB','SCHA','SCHG','SCHV','SCHF','SCHC',
'VTU','VOO','VBK','VB','VEA','VEU','VXUS','VGK','VPL','VWO',
'IWM','XOP','XBI','IAU','SIVR',
'XLE','IIF',
'PSCE','PSCF','PSCM','MLPI','CSO','MLPG','AMJ','MLPN','VQT','RSP','RTM',
'CSD','PWV','PJP','PRF','RPG','RFG',
'IAI','XLF','IAK','OIH','XLE',
'MINDX','MCHFX','NBRFX','NAESX','YAFFX',
'BFGFX','BCSIX','BUFTX','DXRLX','UOPIX','HHBUX','SFENX','SSIFX'
'RGAGX','PRFDX','PRGFX','VINIX','MGOYX','VMGRX','VEVIX','ARTVX','PRNHX','VSCIX','RERGX','APHIX','VTSNX','VTENX','VTHRX','VFORX','VTTSX','PTTRX','PRTXX','VBTIX','VTXVX'
]

[smaArray,emaArray] = _checkSymbols(symbolList)
print smaArray
print emaArray
