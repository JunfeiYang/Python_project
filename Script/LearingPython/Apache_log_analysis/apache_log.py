#!/usr/bin/env python
#coding=utf-8
"""
  Apache Log Parser,
  see module apahcelog:
  http://pypi.python.org/pypi/apachelog/1.0
"""
import re
import sys
import ConfigParser

def getFormat():
    # get 'format' from format.ini
    config = ConfigParser.ConfigParser()
    try:
       inifh = open('format.ini')
    except IOError:
       print "Can not load format.ini !"
       sys.exit(1)
    try:
       options = config.options('format')
    except ConfigParser.NoOptionError:
       print "Can not enum option [format]"
       sys.exit(1)
    for opt in options:
      if opt not in format.keys():
          format[opt] = config.get('format',opt)
      else:
          print "duplicate name in option [format]"
          sys.exit(1)
    try:
       ret = format[formatName]
    except KeyError:
       print "Format /"%s/" has not been defined in format.ini" %formatName
       sys.exit(1)
       return ret

# intercept from module apachelog
class ApacheLogParserError(Exception):
    pass

class parser():
       
  def __init__(self, format):
      self._names = []
      self._regex = None
      self._pattern = ""
      self._parse_format(format)
                                              
  def _parse_format(self, format):
      format = format.strip()
      format = re.sub('[ /t]+',' ',format)


      subpatterns = []


      findquotes = re.compile(r'^//"')
      findreferreragent = re.compile('Referer|User-Agent')
      findpercent = re.compile('^%.*t$')
      lstripquotes = re.compile(r'^//"')
      rstripquotes = re.compile(r'//"$')
      
      for element in format.split(' '):
        hasquotes = 0
        if findquotes.search(element): hasquotes = 1
                       
        if hasquotes:
              element = lstripquotes.sub("", element)
              element = rstripquotes.sub("", element)
        
        self._names.append(self.alias(element))
        
        subpattern = '(/S*)'

        if hasquotes:
           if element == '%r' or findreferreragent.search(element):
              subpattern = r'/"([^"//]*(?://.[^"//]*)*)/"'
           else:
              subpattern = r'/"([^/"]*)/"'
        elif findpercent.search(element):
              subpattern = r'(/[[^/]]+/])'
                                         
        elif element == '%U':
              subpattern = '(.+?)'
                                 

        subpatterns.append(subpattern)
      
      self._pattern = '^' + ' '.join(subpatterns) + '$'
      try:
        self._regex = re.compile(self._pattern)
      except Exception, e:
        raise ApacheLogParserError(e)
  def parse(self, line):
      line = line.strip()
      match = self._regex.match(line)
                       
      if match:
         data = {}
         for k, v in zip(self._names, match.groups()):
             data[k] = v
      return data
      raise ApacheLogParserError("Unable to parse: %s" % line)
  def alias(self, name):
       return name
