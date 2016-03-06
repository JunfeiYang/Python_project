#!/usr/bin/env python
 
import tcpportping
import time
 
i = 0
while i < 5:
    t = tcpportping.tcpping('www.baidu.com', 80, 1000)
    if t < 0:
        print "time out"
    else:
        print t
    time.sleep(0.5)
    i += 1

