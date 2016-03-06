#!/usr/bin/env python
#coding=gb2312 
#-*- encoding: utf-8 -*-
def apache_log(log_path):
	f=open(log_path,'r');
	log=f.readline().rstrip();
	log_home=log.split();
	print log_home;
	ip=log_home[0];
	date=log_home[3].replace('[','');
	point=log_home[5].replace('"','');
	path=log_home[6];
	offer=log_home[8];
	web=log_home[11].replace('"','');
	print ip+'\t'+date+'\t'+point+'\t'+path+'\t'+offer+'\t'+web;
	f.close();
####
if  __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")
	parser.add_option("-u", "--username", dest="username", default='root',
        		  help="USERNAME for ssh_server", metavar="USERNAME")
(options, args) = parser.parse_args()
print 'options: %s, args: %s' % (options, args)
log = apache_log(options.)
print 'apache_log returned %s' % log
sys.exit(not log)
