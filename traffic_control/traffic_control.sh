#!/bin/bash

start_server(){
 rm -f /var/run/traffic_control.pid
 python /root/traffic_control/traffic_control.py > /dev/null &
 ps -ef |grep "python /root/traffic_control/traffic_control.py"|awk '{print $2}' > /var/run/traffic_control.pid
}

stop_server(){
 ps -ef |grep "python /root/traffic_control/traffic_control.py"|awk '{print $2}' |xargs kill -9
 rm -f /var/run/traffic_control.pid
 rm -f /var/run/traffic_control.lock
}




if [ $# == 1 ];then
  case $1 in
   start | START )
     start_server
	;;
   stop |STOP)
     stop_server
	;;
   restart | RESTART )
      stop_server
      start_server
	;;
   * )
     echo "Usage: $0 start|stop|restart"
    esac
else
  echo "Usage: $0 start|stop|restart"
fi
