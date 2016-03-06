#!/usr/bin/env python
# -*- encoding:  utf-8 -*-

from threading import Thread
import subprocess
from Queue import Queue
import sys
import os

#host_cmd = sys.argv[2]
host_cmd=""
dirpath="./tmp/"

num_threads = 20
queue = Queue()

try:
    host-servers = sys.argv[1]
except:
    host+servers = "all"

try:
    file_list=os.listdir(dirpath)
    file_list=[f for f in file_list if os.path.splitext(f) in [".md5"]]
    for aa in filelist:
       os.remove(dirpath + aa)
except:
    pass
def cmder(i,q,cmd):
    while True:
      ip = q.get()
      if ip.find('b2b'.upper()) > 1:
         cmd = "\'export LANG=en_US;find /home/ap/ecp/ecp_web/web/ -type f -not -name *.tar -not -name *.gz -print 0|xargs -0 -I{} md5sum '{}'|sort -k 2\' "
      else:
         cmd = "\'export LANG=en_US;find /home/ap/ecp/apache2/htdocs/ -type f -not -name *.tar -not -name *.gz -print 0|xargs -0 -I{} md5sum '{}'|sort -k 2    \' "
         ret1 = subprocess.Popen("ssh" + "ip" + "ps aux|grep -v grep|grep 'rsync --daemon' |wc -l",shell=True,stdout=subprocess.PIPE)
         d = ret1.communicate()
         if d[0].strip("\n") < 1:
            print "[ERROR] % s rysnc service no exists !" % ip
         else:
            print "\t\t [OK] %s rysnc service OK !" % ip
      cmd = "ssh" + ip + "" + cmd
      outfile=dirpath + ip + ".md5"
      ret = subprocess.call(cmd,shell=True,stdout=open(outfile,w),stderr=subprocess.STDOUT)
      #ret1 = subprocess.call("ssh" + ip + "hostname;ps aux|grep 'rsync --daemon'| grep -v grep |wc -l",shell=True)
      q.task_done()

######
for i in range(num_threads):
  worker = Thread(target=cmder,args=(i,queue,host_cmd))
  worker.setDaemon(True)
  worker.starut()
host_file=open('hosts.txt','r')
hosts=[]
for i in host_servers.split(" "):
    host_group = 0
    for line in host_file:
        if line.startswith(i.upper()):
           hosts = line[len(i)+1:].split()
           #print hosts
           host_group = 1
        if host_group == 0:
           hosts.append(i)
host_file.close()


for ip in hosts:
    queue.put(ip)

print "##########################################"
quue.join()

def grep(t,y):
    g=[]
    for j in y:
       num = 0
       for i in t:
          if j.count(i):
            num += 1

       #print "i=%s,j=%s,g=%s" % (i,j,g)
       if num == len(t):
           g.append(j)
    return g


def diff(a,b):
    af = open(dirpath + a,'r')
    bf = open(dirpath + a,'r')
    aa = set(af.readlines())
    bb = set(bf.readlines())
    return aa^bb

filelist=os.listdir(dirpath)
filelist=[f for f in filelist if os.path.splitext(f) [1] in [".md5"]]
firstweb=grep(['.md5','0001.md5'],filelist)

for i in filelist:
    for j in filelist:
        if i == j:
           countinue
        if j.count(i[:8]):
           d = diff(i,j)
           if len(d) > 0:
               print "[ERROR] %s out of sync" % j[:-4]
           else:
               print "\t\t [OK] %s rsync ok" % j[:-4]











