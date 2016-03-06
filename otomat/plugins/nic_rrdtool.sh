#!/bin/bash
Date=`date "+%Y-%m-%d"`
rrdtool  graphv  nic.png  --start  '-3d' --end '-2d' \
--vertical-label='bytes' \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:%H, \
--width  650  --height  230 \
--title "Network Traffic flow ($Date)" \
DEF:input='nic.rrd':'input':AVERAGE \
DEF:output='nic.rrd':'output':AVERAGE \
DEF:ine='nic.rrd':'input_err':AVERAGE \
DEF:oute='nic.rrd':'output_err':AVERAGE \
COMMENT:" \n" \
CDEF:inp='input,8,*' \
CDEF:outp='output,8,*' \
CDEF:inerr='ine,8,*' \
CDEF:outerr='oute,8,*' \
COMMENT:" \n" \
AREA:inp#FFC125:'Netwrok Input' \
GPRINT:inp:LAST:'Currnet\:%8.2lf' \
GPRINT:inp:AVERAGE:'Average\:%8.2lf' \
GPRINT:inp:MAX:'Maximum\:%8.2lf\n' \
LINE2:outp#CD2626:'Network Output' \
GPRINT:outp:LAST:'Currnet\:%8.2lf' \
GPRINT:outp:AVERAGE:'Average\:%8.2lf' \
GPRINT:outp:MAX:'Maximum\:%8.2lf\n' \
LINE2:inerr#00FF00:'Netwrok Input err' \
GPRINT:inerr:LAST:'Currnet\:%8.2lf' \
GPRINT:inerr:AVERAGE:'Average\:%8.2lf' \
GPRINT:inerr:MAX:'Maximum\:%8.2lf\n' \
LINE3:outerr#0000FF:'Network output err' \
GPRINT:outerr:LAST:'Currnet\:%8.2lf' \
GPRINT:outerr:AVERAGE:'Average\:%8.2lf' \
GPRINT:outerr:MAX:'Maximum\:%8.2lf\n' 
