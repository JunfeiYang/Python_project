#!/bin/bash

start_server(){
 rm -f /var/run/reset_team_port.pid
 python /root/reset_team/reset_team_port.py > /var/log/reset_team_port.log &
 ps -ef |grep "python /root/reset_team/reset_team_port.py"|awk '{print $2}' > /var/run/reset_team_port.pid
}

stop_server(){
 ps -ef |grep "python /root/reset_team/reset_team_port.py"|awk '{print $2}' |xargs kill -9
 rm -f /var/run/reset_team_port.pid
 rm -f /var/run/reset_team_port.lock
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
