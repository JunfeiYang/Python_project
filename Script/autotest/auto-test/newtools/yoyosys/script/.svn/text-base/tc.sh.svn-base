#!/bin/bash

#ipaddr=$1
filepath=$1

action=$2
interval=$3
min=1
loop=$4

if [ ! $filepath ]
then
  echo " usage ./tc.sh filepath action interval [loop]"
  exit 0
fi

if [ ! $action ]
then
  echo " usage ./tc.sh filepath action interval [loop]"
  exit 0
fi

if [ ! $interval ]
then
  echo " usage ./tc.sh filepath action interval [loop]"
  exit 0
fi

if [ ! $loop ]
then
  loop=1
fi
ipaddr=`cat $filepath|tr -d ["\n"]`

source ./common.sh
eths=`geteth $ipaddr`
#echo $eths
if [ ! -n "$eths" ]
then
  echo "no eth"
  exit 0
fi
#echo $action

while [ $min -le $loop ]
do
  if [ $action = delay ] 
  then
    /sbin/tc  qdisc  add  dev  $eths  root  netem  $action  1000ms
  elif [ $action = loss ]
  then
    /sbin/tc  qdisc  add  dev  $eths  root  netem  $action  10%
  elif [ $action = duplicate ]
  then
    /sbin/tc  qdisc  add  dev  $eths  root  netem  $action  1%
  elif [ $action = corrupt ]
  then
    /sbin/tc  qdisc  add  dev  $eths  root  netem  $action  0.3%
  elif [ $action = reorder ]
  then
    /sbin/tc  qdisc  add  dev  $eths  root  netem  delay 10ms $action 25% 50%
  else
    echo "unknown command"
    break
  fi

  min=`expr $min + 1`
  sleep $interval
  /sbin/tc qdisc del dev $eths root

  if [ $min -lt $loop ]
  then
    sleep $interval
  fi

done
