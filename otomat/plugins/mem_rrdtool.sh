#!/bin/bash
Date=`date "+%Y-%m-%d"`
rrdtool  graphv  mem.png  --start  '-3d' --end '-2d' \
--vertical-label='bytes' \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:%H, \
--width  650  --height  230 \
--title "Mem  ($Date)" \
DEF:memtotal='mem.rrd':'mem_total':AVERAGE \
DEF:memfreed='mem.rrd':'mem_freed':AVERAGE \
DEF:memused='mem.rrd':'mem_used':AVERAGE \
DEF:buffersfreed='mem.rrd':'mem_buffers_freed':AVERAGE \
DEF:buffersused='mem.rrd':'mem_buffers_used':AVERAGE \
DEF:mempercent='mem.rrd':'mem_used_percent':AVERAGE \
DEF:swaptotal='mem.rrd':'swap_total':AVERAGE \
DEF:swapfreed='mem.rrd':'swap_freed':AVERAGE \
DEF:swapused='mem.rrd':'swap_used':AVERAGE \
DEF:swappercent='mem.rrd':'swap_used_percnet':AVERAGE \
COMMENT:" \n" \
LINE3:memtotal#FFC125:'Mem Total' \
GPRINT:memtotal:LAST:'Currnet\:%8.2lf %s' \
GPRINT:memtotal:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:memtotal:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:memused#CD2626:'Mem Used' \
GPRINT:memused:LAST:'Currnet\:%8.2lf %s' \
GPRINT:memused:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:memused:MAX:'Maximum\:%8.2lf %s\n' \
LINE2:memfreed#00FF00:'Mem Freed' \
GPRINT:memfreed:LAST:'Currnet\:%8.2lf %s' \
GPRINT:memfreed:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:memfreed:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:buffersfreed#0000FF:'Mem Buffers Freed' \
GPRINT:buffersfreed:LAST:'Currnet\:%8.2lf %s' \
GPRINT:buffersfreed:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:buffersfreed:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:buffersused#EEEE00:'Mem Buffers Used' \
GPRINT:buffersused:LAST:'Currnet\:%8.2lf %s' \
GPRINT:buffersused:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:buffersused:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:mempercent#EE9A49:'Mem Used Percent' \
GPRINT:mempercent:LAST:'Currnet\:%8.2lf %s' \
GPRINT:mempercent:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:mempercent:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:swaptotal#B4EEB4:'SWAP Total' \
GPRINT:swaptotal:LAST:'Currnet\:%8.2lf %s' \
GPRINT:swaptotal:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:swaptotal:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:swapfreed#B4EEB4:'SWAP Freed' \
GPRINT:swapfreed:LAST:'Currnet\:%8.2lf %s' \
GPRINT:swapfreed:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:swapfreed:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:swapused#B4EEB4:'SWAP Used' \
GPRINT:swapused:LAST:'Currnet\:%8.2lf %s' \
GPRINT:swapused:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:swapused:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:swappercent#AAAAAA:'SWAP Used Percent' \
GPRINT:swappercent:LAST:'Currnet\:%8.2lf %s' \
GPRINT:swappercent:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:swappercent:MAX:'Maximum\:%8.2lf %s\n' 
