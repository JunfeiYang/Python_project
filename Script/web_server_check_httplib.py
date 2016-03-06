#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import httplib
import sys
import socket

def check_webserver(address, port, resource):
	#创建 连接
	if not resource.startswith('/'):
	   resource = '/' + resource
	try:
	    conn = httplib.HTTPConnection(address, port) 
	    print 'HTTP connection created successsfully'
	    #make request
	    req = conn.request('GET', resource)
	    print 'request for %s successful' % resource
            # get response
	    response = conn.getresponse()
            print 'response status: %s' % response.status
	except sock.error, e:
	    print 'HTTP connection failed: %s' % e
	    return  False
	finally:
	    conn.close()
	    print 'HTTP connection closed successsfully'
	if response.status in [200, 301]:
	    return True
	else:
	    return False
if __name__ == '__main__':
	from optparse import OptionParser
	websit = "index.html"
	parser = OptionParser(version="0.1beta")
	parser.add_option("-a", "--address", dest="address", default='localhost',
			  help="ADDRESS for webserver", metavar="ADDRESS")
	parser.add_option("-p", "--port", dest="port", default=80,
			  help="PORT for webserver", metavar="PORT")
	parser.add_option("-r", "--resource", dest="resource", default=websit,
			  help="RESOURCE to check", metavar="RESOURCE")
(options, args) = parser.parse_args()
print 'options: %s, args: %s' % (options, args)
check = check_webserver(options.address, options.port, options.resource)
print 'check_webserver returned %s' % check
sys.exit(not check)
