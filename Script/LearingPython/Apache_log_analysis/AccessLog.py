#!/usr/bin/env python
# coding=utf-8
# author : Python[AT]Live.it
import re
import sys
import AccessParse
try:
    LogFile = sys.argv[1]
except IndexError:
    print "Usage : Python %s access.log" %sys.argv[0]
    sys.exit(0)
LogFormat = {
   '%h':'Remote-IP',
   '%l':'Login',
   '%u':'User',
   '%t':'AccessTime',
   '%r':'Request',
   '%>s':'Status',
   '%b':'Bytes',
   '%{Referer}i':'Referer',
   '%{User-Agent}i':'User-Agent'
}

class myParser(AccessParse.parser):
    def __init__(self,format):
        AccessParse.parser.__init__(self,format)
    def alias(self, name):
        return LogFormat[name]
p = myParser(AccessParse.getFormat())
for line in open(LogFile):
  try:
     data = p.parse(line)
     print data
  except AccessParse.ApacheLogParserError,e:
     print "Parser Error , %s" %e
     print "/nMaybe got a bad format in format.ini"
     sys.exit(1)
