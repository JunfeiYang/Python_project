#!/bin/bash

service_name=`ls -l /etc/init.d/|egrep -v 'functions|总用量|total' |awk '{print $NF}'`

for i in $service_name
do
  service $i $1
done

if [ $? == "0" ];then
  reboot
else
  echo "Service failure Stop !"
fi


