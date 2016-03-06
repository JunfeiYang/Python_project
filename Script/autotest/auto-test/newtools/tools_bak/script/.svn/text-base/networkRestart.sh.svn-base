#!/bin/bash

interval=$1
filepath=$2

#ipaddr=$2
min=1
loop=$3

if [ ! $interval ]
then
  echo "usage ./networkRestart.sh interval filepath [loop]"
  exit 0
fi

if [ ! $filepath ]
then
  echo "usage ./networkRestart.sh interval filepath [loop]"
  exit 0
fi

ipaddr=`cat $filepath|tr -d ["\n"]`

if [ ! $loop ]
then
  loop=1
fi

source ./common.sh
eths=`geteth $ipaddr`

#echo "yyyyy="$eths

while [ $min -le $loop ]
do
  /sbin/ifdown $eths
  sleep $interval
  /sbin/ifup $eths

  if [ $min -lt $loop ]
  then
    sleep $interval
  fi

  min=`expr $min + 1`
done
