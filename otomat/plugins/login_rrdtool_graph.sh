#!/bin/bash

rrdtool  graphv  login.png  --start='-2d'  --end='-1d' \
--vertical-label='Users' \
--x-grid MINUTE:12:HOUR:1:HOUR:1:0:%H, \
--width  650  --height  230 \
--title 'Login user (03-19)' \
DEF:o='/var/lib/otomat/172.24.0.27/login_user.rrd':'login_user_num':AVERAGE \
COMMENT:" \n"  \
COMMENT:" \n"  \
AREA:o#00FF00:'Users' \
COMMENT:" "  \
GPRINT:o:LAST:'Currnet\:%8.0lf' \
COMMENT:" "  \
GPRINT:o:AVERAGE:'Avg login user num \:%8.0lf' \
COMMENT:" "  \
GPRINT:o:MAX:'Maximum \:%8.0lf\n' 
