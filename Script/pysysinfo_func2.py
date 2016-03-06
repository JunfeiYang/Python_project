#!/usr/bin/env python
# this is a Gathering script
import subprocess

#cmd1
def uname_func():
	uname = "uname"
	uname_arg = "-a"
	print "Gathering system information with %s command:\n" % uname
	subprocess.call([uname,uname_arg])

#cmd2
def disk_func():
	diskspace = "df"
	diskspace_arg = "-h"
	print "Gathering diskspace information with %s command:\n" % diskspace
	subprocess.call([diskspace,diskspace_arg])
 
def main():
	uname_func()
	disk_func()
main()
