#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import paramiko
import sys
import os
import datetime
#### 
##################
# python 语法帮助模板 sys.argv[0] 代表脚本本身; 测试时采用 print 函数;
# 例如: print sys.argv
# 注意:当脚本执行时需要两个参数,但是脚本本身也算.
#if len(sys.argv) < 2:
#	print "Usage: ", sys.argv[0] ," [username] [ip|hostname] [password] [dir_path] "
#       print  "ex: ", sys.argv[0],"  root 172.16.205.1  XXXXXX  /var/log/message"
#	sys.exit()
#elif len(sys.argv)  < 3:
#        print  "Usage: ", sys.argv[0],  " [ip|hostname] [password] [dir_path]"
#	print  "ex: ", sys.argv[0], " 172.16.205.1 XXXXXX  /var/log/message"
#	sys.exit()
#elif  len(sys.argv)   < 4:
#	print  "Usage: ", sys.argv[0],  " [password] [dir_path]"
#	print  "ex: ", sys.argv[0], "XXXXXX /var/log/message"
#	sys.exit()
#elif  len(sys.argv)  < 5:
#	print  "Usage: ", sys.argv[0],  "[dir_path]"
#       print  "ex: ", sys.argv[0], " /var/log/message" 
#        sys.exit()
#########
def   login_ssh(username, hostname, port, password, dir_path):
	# 定义返回值 可以是数字(0-9),也可以是(字符串)
	ret = 'Successful'
	#定义登陆ssh参数
	#hostname = sys.argv[1]
        hostname = hostname
        port = 22
	#username = sys.argv[2]
        username = username
	#password = sys.argv[3]
        password = password
	#dir_path = sys.argv[4]
        dir_path = dir_path
	#
	t = paramiko.Transport((hostname, port))
        t.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(t)
        try:
          files = sftp.listdir(dir_path)
          for f in files:
            #print 'Retrieving', f
	    #sftp.get(os.path.join(dir_path,f), f)
            print '' 
            print '#########################################' 
            print 'Beginning to download file %s ' % datetime.datetime.now() 
            print 'Downloading file:',os.path.join(dir_path,f)
            # sftp.get(os.path.join(dir_path,f),os.path.join(local_path,f)) 
            sftp.get(os.path.join(dir_path,f), f)
            #sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f)
            print 'Download file success %s ' % datetime.datetime.now() 
            print '' 
            print '##########################################'  
        except :
	     ret = Failure
	finally:
	  t.close()
	  return ret

####
if  __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")
	parser.add_option("-u", "--username", dest="username", default='root',
        		  help="USERNAME for ssh_server", metavar="USERNAME")
	parser.add_option("-a", "--address", dest="hostname", default='localhost',
			  help="ADDRESS for ssh_server", metavar="ADDRESS")
	parser.add_option("-p", "--port", dest="port", default='22',
			  help="PORT for ssh_server", metavar="PORT")
	parser.add_option("-P", "--password", dest="password", default='password',
			  help="PASSWORD for ssh_server", metavar="PASSWORD")
	parser.add_option("-d", "--directory", dest="dir_path", default='/tmp',
			  help="Documents directory", metavar="DIRECTORY")
(options, args) = parser.parse_args()
print 'options: %s, args: %s' % (options, args)
ssh = login_ssh(options.username, options.hostname, options.port, options.password, options.dir_path)
print 'login_ssh returned %s' % ssh
sys.exit(not ssh)
