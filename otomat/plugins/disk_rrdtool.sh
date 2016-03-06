#!/bin/bash
Date=`date "+%Y-%m-%d"`
rrdtool  graphv  disk.png  --start  '-2d' --end '-1d' \
--vertical-label='bytes' \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:%H, \
--width  650  --height  230 \
--title "Disk Space ($Date)" \
DEF:percent='disk.rrd':'disk_used_percnet':AVERAGE \
DEF:used='disk.rrd':'disk_used':AVERAGE \
DEF:freed='disk.rrd':'disk_freed':AVERAGE \
DEF:total='disk.rrd':'disk_total':AVERAGE \
COMMENT:" \n" \
AREA:percent#FFC125:'Percent' \
GPRINT:percent:LAST:'Currnet\:%8.2lf %s' \
GPRINT:percent:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:percent:MAX:'Maximum\:%8.2lf %s\n' \
AREA:used#CD2626:'Used' \
GPRINT:used:LAST:'Currnet\:%8.2lf %s' \
GPRINT:used:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:used:MAX:'Maximum\:%8.2lf %s\n' \
LINE2:freed#00FF00:'Freed' \
GPRINT:freed:LAST:'Currnet\:%8.2lf %s' \
GPRINT:freed:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:freed:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:total#0000FF:'Total' \
GPRINT:total:LAST:'Currnet\:%8.2lf %s' \
GPRINT:total:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:total:MAX:'Maximum\:%8.2lf %s\n' 
