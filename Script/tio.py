#!/usr/bin/env python

#kevx@2013/2/24

import sys
import os

        
rwTop = {}

class Rw(object):
    def __init__(self, tid, r, w):
        self._tid = tid
        self._r = r
        self._w = w
        return
    
    def tid(self):
        return self._tid
    def writecnt(self):
        return self._w
    def readcnt(self):
        return self._r
    def add_read(self, n):
        self._r = self._r + n
    def add_write(self, n):
        self._w = self._w + n
        
    def __eq__(self, other):
        if other == None:
            return False
        return self._tid == other._tid

    def __hash__(self):
        return hash(self._tid)

###############################
def parse_file(iofile, tid):
    fp = open(iofile)
    try:
        rw = Rw(tid, 0, 0)
        lines = fp.readlines()
        if lines is None: return
        for line in lines:
            if line.startswith('read_bytes:'):
                rw.add_read(int(line[11:]))
                continue
                
            if line.startswith('write_bytes:'):
                rw.add_write(int(line[12:]))
                continue
        return rw
        
    finally:
        fp.close()
    return None

###############################        
def one_loop(pid):
    s = '/proc/%d/task'%(pid)
    ts = os.listdir(s)
    for t in ts:
        iofile = '%s/%s/io'%(s, t)
        tid = int(t)
        rw = parse_file(iofile, tid)
        rwTop[tid] = rw

############################### 

def top_read():
    print 'Top 10 bytes-read threads:' 
    key = lambda x:x.readcnt()
    l = sorted(list(rwTop.values()), key=key, reverse=True)
    for i in range(10):
        print '#%d:%d:%d'%(i, l[i].tid(), l[i].readcnt())
    
def top_write():
    print 'Top 10 bytes-write threads:' 
    key = lambda x:x.writecnt()
    l = sorted(list(rwTop.values()), key=key, reverse=True)
    for i in range(10):
        print '#%d:%d:%d'%(i, l[i].tid(), l[i].writecnt())
       
def main():
    print "-----------------"
    print "Threads IO STAT"
    print "-----------------"
    one_loop(int(sys.argv[1]))
    top_read()
    top_write()
        
if __name__ == '__main__':
    main()











#File info
#Size: 2158 bytes, 93 lines
#View raw file

