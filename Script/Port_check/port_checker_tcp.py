#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#========================================================================
# Author:Junfei Yang
# Email:yangjunfei2146@gmail.com
# File Name:
# Description:  
# Edit History:
#2012-09-27 File created.
#========================================================================
import socket
import re
import sys

def check_server(address, port):
	#Create a tcp socket
	s = socket.socket()
	print "Attempting to connect %s on port %s" % (address, port)
	try:
	  s.connect((address, port))
	  print "Connected to %s on port %s" % ((address, port))
	  return True
	except socket.error, e:
	  print "Connection to %s on port %s failed: %s" % (address, port, e)
	  return False

if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")

	parser.add_option("-a", "--address", dest="address", default='localhost',
			  help="ADDRESS for server", metavar="ADDRESS")
	parser.add_option("-p", "--port", dest="port", type="int", default=80,
			  help="PORT for server", metavar="PORT")

(options, args) = parser.parse_args()
#options, args = parser.parse_args()
print 'options: %s, args: %s' % (options, args)
check = check_server(options.address, options.port)
print 'check_server returned %s' % check
sys.exit(not check)
