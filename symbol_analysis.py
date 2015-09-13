#!/usr/bin/env python


import time
import sys
from datetime import date

class symbol_analysis(object):
    def __init__(self,symbol,sma_ptr):
        self.symbol = symbol;
        self.sma_ptr = sma_ptr;
        self._price_row = [];
        self._sma_row = [];
        self._name = ""
        self._trend = 0
        self._reverseTrend = 0
        self._peakVal = 0
        self._curPrice = 0.0
        self._prevPrice = 0.0
        self._crossing = 0.0
        self._pctage_diff = 0.0
        self._newTrend = 0
        self._200dayPct = 0
        self._trendSpeed = 0
        self._trendSlope = 0
        self._price_row = self.sma_ptr._find_price_list(self.symbol);
        self._sma_row   = self.sma_ptr._find_sma_list(self.symbol);
        self._name   =    self.sma_ptr._find_name(self.symbol);
        self._100_day_high = 0.0
        self._100_day_roc = 0.0
        self._daily_chg = 0

    def _print(self):
        print "Name = %s" % (self._name)

    def _trend_reversal(self):
        startSma = float(self._sma_row[self.sma_ptr.numSma])
        latestSma = float(self._sma_row[1])
        if (startSma < latestSma):
            self._trend = 1
            self._reverseTrend = 0
        self._newTrend = self._trend
        for i in range (7,33):
            val = float(self._sma_row[i])
            if self._trend: 
                if ((val > latestSma) | (val < startSma)):
                    self._reverseTrend = 1
                    if (val > latestSma):
                        self._newTrend = 0
                    if (val > self._peakVal):
                        self._peakVal = val;
                if (val < startSma):
                     self._newTrend = 1
                if (val < self._peakVal):
                     self._peakVal = val;
            else: 
                 if ((val < latestSma) | (val > startSma)):
                     self._reverseTrend = 1
                 if (val < latestSma):
                      self._newTrend = 1
                 if (val < self._peakVal):
                     self._peakVal = val;
                 if (val > startSma):
                     self._newTrend = 0
                 if (val > self._peakVal):
                     self._peakVal = val;

    def _slope_calc(self, row):
        if self._trend:
            slope = (float(row[0]) - float(row[19]))/20
        else:
            slope = (float(row[19]) - float(row[0]))/20
        return slope

    def _find_100_day_high(self):
        curMax = float(self._price_row[1])

        for i in range (1,101):
            if (float(self._price_row[i]) > curMax):
                curMax = float(self._price_row[i])

        self._100_day_high = curMax
        return curMax

    def _find_100_day_roc(self):
        curPrice      = float(self._price_row[1])
        priceMinus100 = float(self._price_row[101])
        roc = int(((curPrice - priceMinus100)* 100) / priceMinus100 )
        self._100_day_roc = roc
        return roc

    def _price_analysis(self):
        self._curPrice = float(self._price_row[1])
        self._prevPrice = float(self._price_row[2])
        curSma = float(self._sma_row[1])
        self._crossing = 0
        if (self._curPrice > curSma):
            if (curSma > self._prevPrice):
                self._crossing = 1
        else:
            if (curSma < self._prevPrice):
                self._crossing = 2

        price200 = float(self._price_row[200])
        self._200dayPct = int(((self._curPrice - price200)*100) / price200)
        self._pctage_diff = ((self._curPrice - curSma)*100.0) / self._curPrice
        self._find_100_day_roc();
        self._find_100_day_high();

    def _trend_shape(self):
        trendSlope = 0
        trendSpeed = 0
        if self._reverseTrend:
            startSma = float(self._sma_row[self.sma_ptr.numSma])
            latestSma = float(self._sma_row[1])
                      # Compute model is different here
            if (self._newTrend):
                pctChng = ((latestSma - self._peakVal)*100.0)/latestSma
            else:
                pctChng = ((self._peakVal - latestSma)*100.0)/latestSma
                
        else:
            slope_20 =  self._slope_calc(self._sma_row[1:21])   
            slope_40 =  self._slope_calc(self._sma_row[21:41])  
            startSma = float(self._sma_row[self.sma_ptr.numSma])
            latestSma = float(self._sma_row[1])
            if self._trend:
                pctChng = ((latestSma - startSma)*100.0)/latestSma
            else:
                pctChng = ((startSma - latestSma)*100.0)/latestSma

            if (slope_20 > slope_40):
                trendSlope = 1
    
        if (pctChng > 8.0):
            trendSpeed = 1
        self._trendSpeed = trendSpeed;
        self._trendSlope = trendSlope;
        return trendSpeed,trendSlope

    def _check_pctg_diff(self):
        self._daily_chg = int((abs(self._curPrice - self._prevPrice)*100.0) / self._prevPrice)

    def _analyze(self):
        self._trend_reversal()
        self._price_analysis()
        self._check_pctg_diff()
        (trendSpeed,trendSlope) = self._trend_shape()

        name = self._name
        name += " %6d " % (self._curPrice)
        if (self._curPrice > self._prevPrice):
            name += "+"
            name += "%.4d" %(self._curPrice-self._prevPrice)
        else:
            name += "-"
            name += "%.4d" %(self._prevPrice-self._curPrice)

        if self._reverseTrend:
            trendStr = "reverses to "
            if (self._newTrend):
                trendStr += "rising"
            else:
                trendStr += "falling"
        else:
            if self._trend:
                trendStr = "rising"
            else:
                trendStr = "falling"

        if (self._crossing == 1):
            smaStr = "crossed above 200dma "
        elif (self._crossing == 2):
            smaStr = "crossed below 200dma "
        else:
            if (self._pctage_diff < 0.0):
                smaStr = "%2s pct below SMA" % (int(self._pctage_diff) * -1)
            else:
                smaStr = "%2s pct above SMA" % (int(self._pctage_diff))

        if trendSpeed:
            trendShape = "sharp"
        else:
            trendShape = "slow"

        if (not self._reverseTrend):
            if trendSlope:
                trendShape += " Accelerating trend "
            else:
                trendShape += " decelerating trend "

        signalType = "N"
        if ((self._curPrice >= self._100_day_high) & (self._100_day_roc > 25)):
            signalType = "B"

        retString = "%-6s %45s %-20s %-23s %s %2s %s %2s %s" % (self.symbol, name, trendStr, smaStr, trendShape, self._200dayPct, self._100_day_high, self._100_day_roc, signalType);
        print retString;
        return retString;

    def _find_adj(self):
        #print "Check Adjust for %s" % self.symbol
        prevPrice = float(self._price_row[1])
        adjFound = 0
        #for val in self._price_row:
        for val in range (2,len(self._price_row) - 1):
            curPrice = float(self._price_row[val])
            priceDiff = abs(curPrice - prevPrice)
            if (priceDiff/curPrice) > 0.1:
                 if (adjFound == 0):
                     print "Potential Adjustment required %s - %s %s\n" % (self.symbol, curPrice, prevPrice)
                 adjFound = 1
            prevPrice = curPrice;
        return adjFound

    def _adj_price(self):
        #print "Check Adjust for %s" % self.symbol
        retArr = [];
        retArr.append(self._price_row[0]);
        retArr.append(self._price_row[1]);
        prevPrice = float(self._price_row[1])
        adjFound = 0
        adjRatio = 0
        for val in range (2,len(self._price_row)):
            curPrice = float(self._price_row[val])
            if (adjFound):
                newPrice = curPrice * adjRatio
            else:
                priceDiff = abs(curPrice - prevPrice)
                newPrice = curPrice
            if (priceDiff/curPrice) > 0.1:
                 adjRatio = prevPrice/curPrice
                 adjFound = 1;
                 newPrice = curPrice * adjRatio
            prevPrice = curPrice;
            retArr.append(newPrice)
        return retArr

    def _check_triggers(self, trigDet):
        self._print()
        curPrice = float(self._price_row[1])
        tt = trigDet['triggerType']
        retType = 'F'
        if (tt == "R"):
            lv = float(trigDet['lowVal'])
            hv = float(trigDet['highVal'])
            if (lv > curPrice) | (hv < curPrice):
                retType = 'T'
            retString = "%s %s < %s < %s %s" % (self.symbol, trigDet['lowVal'], curPrice, trigDet['highVal'], retType)
        elif (tt == "LT"):
            lv = float(trigDet['lowVal'])
            if (lv > curPrice):
                retType = 'T'
            retString = "%s %s < %s %s" % (self.symbol, curPrice, trigDet['lowVal'], retType)
        elif (tt == "GT"):
            hv = float(trigDet['highVal'])
            if (hv < curPrice):
                retType = 'T'
            retString = "%s %s > %s %s" % (self.symbol, curPrice, trigDet['highVal'], retType)
        else:
            retString = "%s %s %s %s " % (self.symbol, trigDet['triggerType'], trigDet['highVal'], trigDet['lowVal'])
        return retType,retString
