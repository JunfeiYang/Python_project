#!/bin/bash

ports=$1
interval=$2
min=1
loop=$3

/sbin/iptables -F
/sbin/iptables -P INPUT ACCEPT
/sbin/iptables -P FORWARD ACCEPT
/sbin/iptables -P OUTPUT ACCEPT

if [ ! $loop ]
then
  loop=1
fi

if [ ! $interval ]
then 
  echo "Usage : ./iptable.sh $shell ports interval [loop]"
  exit 0
fi

while [ $min -le $loop ]
do
  #echo $min
  /sbin/iptables -A INPUT -p tcp --dport $ports -s 172.16.0.0/16 -j REJECT --reject-with tcp-reset
  /sbin/iptables -A OUTPUT -p tcp --dport $ports -d 172.16.0.0/16 -j REJECT --reject-with tcp-reset
  /sbin/iptables -A OUTPUT -p tcp --sport $ports -d 172.16.0.0/16 -j REJECT --reject-with tcp-reset

  /sbin/iptables -A INPUT -p udp --dport $ports -s 172.16.0.0/16 -j REJECT
  /sbin/iptables -A OUTPUT -p udp --sport $ports -d 172.16.0.0/16 -j REJECT
  /sbin/iptables -A OUTPUT -p udp --dport $ports -d 172.16.0.0/16 -j REJECT
  #echo "cut"
  sleep $interval
  /sbin/iptables -F
  #echo "recovery" 

  if [ $min -lt $loop ]
  then
  sleep $interval
  fi
  min=`expr $min + 1`
done
 
