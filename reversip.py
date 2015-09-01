#!/usr/bin/env python

import urllib2
import socket
import sys
import re

class reverseip(object):

           def __init__(self, server='http://www.ip-adress.com/reverse_ip/'):
               t= """ Tool made by: LeXeL lexelEZ[at]gmail[dot]com """
               print t

               try:
                   self.site = raw_input("Enter site to start scan: ")
                   self.fileout = raw_input("Enter logfile name: ")
               except KeyboardInterrupt:
                   print "\n\nError: Aborted"
                   sys.exit(1)

               self.server = server
               self.ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"
               self.h = {"User-Agent": self.ua}

               self.write = True
               try:
                     outp = open(self.fileout, "w+")
                     outp.write(t)
                     outp.close()
               except IOError:
                     print '\n Failed to write to %s' % (self.fileout)
                     print '\n Continuing without writing'
                     self.write = False


           def url(self):
                    r = urllib2.Request('%s%s' % (self.server, self.site), headers=self.h)
                    f = urllib2.urlopen(r)
                    self.source = f.read()

           def getip(self):
                    try:
                        ip = socket.gethostbyname(self.site)
                    except IOError, e:
                        print "Error: %s " %(e)
                    else:      
                        print "\t\nScanning ip %s \n\n" %(ip)

if __name__ == '__main__':
     p = reverseip()
     p.url()
     p.getip()
