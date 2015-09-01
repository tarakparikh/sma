#!/usr/bin/env python

import xml.etree.ElementTree as ET

def read_portfolio(filename):
    xmlroot = ET.parse(filename)
    treeroot = xmlroot.getroot()
    myarray = []
    for stock in treeroot:
	    #print stock
	    #print stock.get('symbol')
	    myhash = {};
	    myhash['symbol'] = stock.get('symbol')
	    for mm in stock:
		    myhash[mm.tag] = mm.text
	    myarray.append(myhash)

    return myarray
    

#myportfolio = read_portfolio(".mgc.xml")
#for ix1 in myportfolio:
	    #print ix1
