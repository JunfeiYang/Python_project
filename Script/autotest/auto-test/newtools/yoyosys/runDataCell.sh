#!/bin/sh

export RELEASE_HOME=/root/YoyoSoft/modules/smartstorage_datacell
export YOYO_LOG_DIR=/root/YoyoSoft/modules/smartstorage_datacell/logs

ulimit -c unlimited
ulimit -n 102400
. $RELEASE_HOME/bf_setenv.sh
export YOYO_DEFAULT_LOG_LVL=Debug
export YOYO_LOG_CORE_DHT=Debug
export YOYO_LOG_DATACELL_GENERAL=Debug
export YOYO_LOG_DATACELL_BACKEND=Debug
export YOYO_LOG_DATACELL_DAEMON=Debug
export YOYO_LOG_DATACELL_API=Debug
export YOYO_LOG_CORE_FILE=Debug
export YOYO_LOG_DATACELL_TIME_SERIES_BACKEND=Debug
export YOYO_LOG_DATACELL_FILE_SYSTEM_BACKEND=Debug
#export YOYO_DEFAULT_LOG_LVL=Debug
export YOYO_LOG_ROTATION_LINES=104857600
export YOYO_LOG_ROTATION_FILES=5
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RELEASE_HOME/lib:/usr/lib:/usr/local/lib

$RELEASE_HOME/bin/DataCell -d -logfile $YOYO_LOG_DIR/datacell.log -cfgfile $RELEASE_HOME/conf/DataCell.xml -pidfile $YOYO_LOG_DIR/datacell.pid