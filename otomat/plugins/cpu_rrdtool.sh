#!/bin/bash
Date=`date "+%Y-%m-%d"`
rrdtool  graphv  cpu.png  --start  '-2d' --end '-1d' \
--vertical-label='bytes' \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:%H, \
--width  650  --height  230 \
--title "CPU  Utilization rate ($Date)" \
DEF:a='cpu.rrd':'cpu_loadavg_1':AVERAGE \
DEF:b='cpu.rrd':'cpu_loadavg_5':AVERAGE \
DEF:c='cpu.rrd':'cpu_loadavg_15':AVERAGE \
DEF:user='cpu.rrd':'cpu_user':AVERAGE \
DEF:nic='cpu.rrd':'cpu_nice':AVERAGE \
DEF:system='cpu.rrd':'cpu_system':AVERAGE \
DEF:iowait='cpu.rrd':'cpu_iowait':AVERAGE \
DEF:steal='cpu.rrd':'cpu_steal':AVERAGE \
DEF:idel='cpu.rrd':'cpu_idel':AVERAGE \
COMMENT:" \n" \
LINE3:a#FFC125:'Loadavg 1'  \
GPRINT:a:LAST:'Currnet\:%8.2lf %s'  \
GPRINT:a:AVERAGE:'Average\:%8.2lf %s'  \
GPRINT:a:MAX:'Maximum\:%8.2lf %s\n'  \
LINE3:b#EE7600:'Loadavg 5' \
GPRINT:b:LAST:'Currnet\:%8.2lf %s' \
GPRINT:b:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:b:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:c#FF0000:'Loadavg 15' \
GPRINT:c:LAST:'Currnet\:%8.2lf %s' \
GPRINT:c:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:c:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:user#0000FF:'CPU User' \
GPRINT:user:LAST:'Currnet\:%8.2lf %s' \
GPRINT:user:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:user:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:nic#9AC0CD:'CPU Nice' \
GPRINT:nic:LAST:'Currnet\:%8.2lf %s' \
GPRINT:nic:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:nic:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:system#9A32CD:'CPU System' \
GPRINT:system:LAST:'Currnet\:%8.2lf %s' \
GPRINT:system:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:system:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:iowait#999999:'CPU Iowait' \
GPRINT:iowait:LAST:'Currnet\:%8.2lf %s' \
GPRINT:iowait:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:iowait:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:steal#9AC0CD:'CPU Steal' \
GPRINT:steal:LAST:'Currnet\:%8.2lf %s' \
GPRINT:steal:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:steal:MAX:'Maximum\:%8.2lf %s\n' \
LINE3:idel#00CD00:'CPU Idel' \
GPRINT:idel:LAST:'Currnet\:%8.2lf %s' \
GPRINT:idel:AVERAGE:'Average\:%8.2lf %s' \
GPRINT:idel:MAX:'Maximum\:%8.2lf %s\n' \
